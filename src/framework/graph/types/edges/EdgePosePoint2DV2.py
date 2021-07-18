import typing as tp

from src.framework.graph.types.edges.CalibratingEdgeSE2 import CalibratingEdgeSE2
from src.framework.graph.types.nodes.SpatialNode import NodeSE2
from src.framework.graph.types.nodes.SpatialNode import NodeV2
from src.framework.math.lie.transformation import SE2
from src.framework.math.matrix.square import Square3
from src.framework.math.matrix.vector import Vector2


class EdgePosePoint2DV2(CalibratingEdgeSE2):
    _num_topological = 2

    def __init__(
            self,
            value: tp.Optional[SE2] = None,
            info_matrix: tp.Optional[Square3] = None,
            node_a: tp.Optional[NodeSE2] = None,
            node_b: tp.Optional[NodeV2] = None
    ):
        nodes = list(filter(lambda n: n is not None, [node_a, node_b]))
        super().__init__(value, info_matrix, *nodes)

    def get_value(self) -> Vector2:
        a: NodeSE2
        b: NodeV2
        a, b = tuple(self.get_endpoints())
        return Vector2(b.get_value() - a.get_value().translation())