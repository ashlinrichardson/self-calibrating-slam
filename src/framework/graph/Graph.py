import pathlib
from datetime import datetime
from typing import *

from src.framework.graph.factor.FactorEdge import FactorEdge
from src.framework.graph.factor.FactorGraph import FactorGraph
from src.framework.graph.factor.FactorNode import FactorNode
from src.framework.graph.types import *


class Graph(FactorGraph):

    # constructor
    def __init__(self, id: Optional[int] = 0, name: Optional[str] = None):
        super().__init__()
        self._types = self._init_types()
        self._id = id
        self._name = None

    # initialisation
    @staticmethod
    def _init_types() -> Dict[str, Any]:
        types: Dict[str, Any] = dict()
        types['VERTEX_SE2'] = NodeSE2
        types['EDGE_SE2'] = EdgeSE2
        types['VERTEX_POINT_XY'] = NodeXY
        types['EDGE_SE2_POINT_XY'] = EdgeSE2XY
        return types

    # getters/setters
    def get_id(self) -> int:
        assert self._id is not None
        return self._id

    def set_id(self, id: int):
        self._id = id

    def get_name(self, short: bool = False):
        if self._name is None:
            return '{}_Graph'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))
        else:
            if short:
                return pathlib.Path(self._name).name
            return self._name

    # load/save methods
    def load(self, filename: str):
        self._name = filename
        print('Reading file: {}'.format(filename))
        file = open(filename, 'r')
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line == '\n':
                raise Exception('Empty line {}'.format(i + 1))
            line = line.strip()
            words = line.split()

            # handle FIX

            token = words[0]
            assert token in self._types
            element_type = self._types[token]

            # handle parameters

            if issubclass(element_type, FactorNode):
                id = int(words[1])
                node = element_type(id)
                rest = words[2:]
                node.read(rest)
                self.add_node(node)
            elif issubclass(element_type, FactorEdge):
                size = element_type.size
                ids = words[1: 1 + size]
                nodes = [self.get_node(int(id)) for id in ids]
                edge = element_type.from_nodes(nodes)
                rest = words[1 + size:]
                edge.read(rest)
                self.add_edge(edge)

    def save(self, filename: str):
        self._name = filename
        print('Saving to file: {}'.format(filename))
        file = pathlib.Path(filename)
        if file.exists():
            file.unlink()
        writer = open(filename, 'x')

        for node in self.get_nodes():
            writer.write(node.write() + '\n')
        for edge in self.get_edges():
            writer.write(edge.write() + '\n')

    # object methods
    def __str__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.get_id(), self.id_string())