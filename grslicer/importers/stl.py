from struct import unpack

import vertexmerger
from grslicer.model import TopoModel
from grslicer.util.np import to_ndarray
from grslicer.importers.base import ModelImporter
from grslicer.util.progress import progress_log


class StlAsciiImporter(ModelImporter, vertexmerger.VertexMerger):
    @staticmethod
    def can_import(contents):
        return all([kw in contents for kw in ('solid', 'vertex', 'facet normal')])

    def __init__(self, *args, **kwargs):
        super(StlAsciiImporter, self).__init__(*args, **kwargs)

        self.vertex_nr = self._get_face_nr() * 3

        self.merger = vertexmerger.VertexMerger(TopoModel(shape=(self.vertex_nr * 3, 3)),
                                                self.settings.roundOffError)

    def _get_face_nr(self):
        return self.contents.count('facet normal')

    @property
    def tm(self):
        return self.merger.tm

    @progress_log('Importing ASCII STL file contents')
    def import_contents(self, progress):

        progress.set_size(self.vertex_nr)

        vertex_kw = 'vertex'
        for line in self.contents.splitlines():
            if vertex_kw in line:
                # parse vector coordinates
                vector = to_ndarray([float(x) for x in line.strip().split()[-3:]])
                self.merger.add(vector)

                progress.inc()

        self.merger.finalize()

        progress.done()

        return self.tm


class StlBinImporter(StlAsciiImporter):
    @staticmethod
    def can_import(contents):
        # TODO: check for characters that are >127, see three.js STL importer
        return not StlAsciiImporter.can_import(contents)

    def _get_face_nr(self):
        return (len(self.contents) - 84) / 50

    @progress_log('Importing BIN STL file contents')
    def import_contents(self, progress):

        progress.set_size(self.vertex_nr)

        byte_idx = 84

        for face_idx in range(self._get_face_nr()):
            for vertex_idx in range(1, 4):
                vector = to_ndarray(self._parse_vector(byte_idx + 12 * vertex_idx))
                self.merger.add(vector)

                progress.inc()

            byte_idx += 50

        self.merger.finalize()

        progress.done()

        return self.tm

    def _parse_vector(self, position):
        xyz = []
        for coordinate_index in range(3):
            pos_start = position + coordinate_index * 4
            xyz.append(unpack('f', self.contents[pos_start: pos_start + 4])[0])
        return xyz