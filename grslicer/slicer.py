""" Slice D3TopoModel with horizontal planes and create contours
"""

from grslicer.model import Layer, LayeredModel
from grslicer.util.np import np_range, to_ndarray
from grslicer.util import cynp
from grslicer.patterns.infill import fill_layer
from grslicer.util.progress import progress_log


def slice_model(tm, settings):
    slicer = FixedLayerHeightSlicer(tm, settings)
    slicer.slice()
    return slicer.model


class FixedLayerHeightSlicer(object):
    def __init__(self, tm, settings):
        self.tm = tm
        self.s = settings
        self._slicing_positions = None  # should be private
        self._edge_map = {}  # should be private
        self.model = LayeredModel(aabb=tm.aabb)

    def _init_slicing_positions(self):
        """ Returns heights at which model should be sliced. Starts at <layer_height>
        """
        aabb = self.tm.aabb
        self._slicing_positions = np_range(aabb.min[2] + self.s.layerHeight, aabb.max[2], self.s.layerHeight)

    def _init_edge_height_map(self):
        lh = self.s.layerHeight
        bottom = self._slicing_positions[0] - lh
        for edge in self.tm.edges.values():
            h1 = edge.vertex_a.vector[2]
            h2 = edge.vertex_b.vector[2]

            if h1 != h2:
                if h1 > h2:
                    h1, h2 = h2, h1
                # find intersections with slicing positions
                idx_start = int((h1 - bottom) // lh)
                if idx_start > 0:
                    idx_start -= 1
                idx_end = int((h2 - bottom) // lh) + 1
                for h in self._slicing_positions[idx_start:idx_end]:
                    if h1 < h <= h2:
                        self._edge_map.setdefault(h, set()).add(edge.mxid)

    @progress_log('Slicing model with fixed layer heights')
    def slice(self, progress):
        self._init_slicing_positions()

        progress.set_size(len(self._slicing_positions))

        self._init_edge_height_map()

        for i, h in enumerate(sorted(self._edge_map.keys())):

            contours = []

            # edges that need to be visited on this height
            to_visit = self._edge_map[h]
            while len(to_visit) > 0:
                # 2D path - z coordinate is omitted as it is represented as height
                contour = []

                prev_face = None
                edge = self.tm.edges[to_visit.pop()]

                while True:

                    # intersect the edge
                    intersection = _edge_2d_intersection(edge, h)
                    contour.append(intersection)

                    to_visit.discard(edge.mxid)

                    # march
                    if prev_face is None:
                        # doesn't matter which face
                        prev_face = edge.face_a
                    else:
                        # select the opposite from the one we came
                        prev_face = edge.face_b if prev_face is edge.face_a else edge.face_a

                    # select edge from edges of a face that has not yet been worked on
                    edge = next((e for e in prev_face.edges if e.mxid in to_visit), None)

                    # contour is finished when there is no more edges to cut
                    # WARNING: if the topology of the model is not manifold (holes in mesh)
                    # it might happen that the contour will be closed too soon
                    if edge is None:
                        break

                # All contours are closed
                contours.append(to_ndarray(contour))

            if contours:
                self.add_layer(contours, h, i)

            progress.inc()

        progress.done()

    def add_layer(self, contours, height, seq_nr):
        layer = Layer(self.model, height, seq_nr)
        fill_layer(layer, contours, self.s, self.model)
        self.model.layers[seq_nr] = layer


def _edge_2d_intersection(edge, h):
    return cynp.edge_intersection(edge.vertex_a.vector, edge.vertex_b.vector, h)
