from src.framework.graph.types.scslam2d.nodes.CalibratingNode import CalibratingNode
from src.framework.math.matrix.vector import Vector2


class NodeV2(CalibratingNode[Vector2]):

    _type = Vector2
