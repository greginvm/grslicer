from struct import unpack


import vertexmerger
from grslicer.model import TopoModel
from grslicer.util.np import to_ndarray
from grslicer.importers.base import ModelImporter


class StlAsciiImporter(ModelImporter, vertexmerger.VertexMerger):
    @staticmethod
    def can_import(contents):
        return all([kw in contents for kw in ('solid', 'vertex', 'facet normal')])

    def __init__(self, *args, **kwargs):
        super(StlAsciiImporter, self).__init__(*args, **kwargs)
        self.merger = vertexmerger.VertexMerger(TopoModel(shape=(self._get_face_nr() * 3, 3)),
                                                self.settings.roundOffError)

    def _get_face_nr(self):
        return self.contents.count('facet normal')

    @property
    def tm(self):
        return self.merger.tm

    def import_contents(self):
        vertex_kw = 'vertex'
        for line in self.contents.splitlines():
            if vertex_kw in line:
                # parse vector coordinates
                vector = to_ndarray([float(x) for x in line.strip().split()[-3:]])
                self.merger.add(vector)

        self.merger.finalize()
        return self.tm


class StlBinImporter(StlAsciiImporter):
    @staticmethod
    def can_import(contents):
        # TODO: check for characters that are >127, see three.js STL importer
        return not StlAsciiImporter.can_import(contents)

    def _get_face_nr(self):
        return (len(self.contents) - 84) / 50

    def import_contents(self):
        byte_idx = 84

        for face_idx in range(self._get_face_nr()):
            for vertex_idx in range(1, 4):
                vector = to_ndarray(self._parse_vector(byte_idx + 12 * vertex_idx))
                self.merger.add(vector)

            byte_idx += 50

        self.merger.finalize()
        return self.tm

    def _parse_vector(self, position):
        xyz = []
        for coordinate_index in range(3):
            pos_start = position + coordinate_index * 4
            xyz.append(unpack('f', self.contents[pos_start: pos_start + 4])[0])
        return xyz