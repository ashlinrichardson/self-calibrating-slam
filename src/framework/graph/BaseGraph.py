import typing as tp

from src.framework.graph.protocols.Printable import Printable
from src.utils.TypeDict import TypeDict

Node = tp.TypeVar('Node', bound='BaseNode')
Edge = tp.TypeVar('Edge', bound='BaseEdge')
Element = tp.Union[Node, Edge]


class BaseGraph(tp.Generic[Node, Edge], Printable):

    def __init__(self):
        self._nodes: tp.Dict[int, Node] = {}
        self._edges: tp.List[Edge] = []
        self._nodes_sorted = TypeDict()
        self._edges_sorted = TypeDict()

    # nodes
    def add_node(self, node: Node) -> None:
        assert not self.contains_id(node.get_id()), f'Node with {node.get_id()} already present in {self.to_unique()}.'
        self._nodes[node.get_id()] = node
        self._nodes_sorted.add(node)

    def get_nodes(self) -> tp.List[Node]:
        return list(self._nodes.values())

    def get_node(self, id_: int) -> Node:
        assert self.contains_id(id_), f'{id_} not present in {self.to_unique()}.'
        return self._nodes[id_]

    def contains_id(self, id_: int) -> bool:
        return id_ in self._nodes

    # edges
    def add_edge(self, edge: Edge) -> None:
        for node in edge.get_nodes():
            assert self.contains_id(node.get_id()), f'{node.to_name()} with id {node.get_id()} is not present in {self.to_unique()}.'
        assert edge not in self.get_edges(), f'{edge.to_unique()} already present in {self.to_unique()}.'
        self._edges.append(edge)
        self._edges_sorted.add(edge)

    def get_edges(self) -> tp.List[Edge]:
        return self._edges

    # elements
    def get_elements_of_type(self, type_: tp.Type[Element]) -> tp.List[Element]:
        if type_ in self._nodes_sorted:
            return self._nodes_sorted[type_]
        if type_ in self._edges_sorted:
            return self._edges_sorted[type_]

    # Printable
    def to_id(self) -> str:
        return f'{len(self._nodes)}; {len(self._edges)}'


class BaseNode(Printable):

    def __init__(
            self,
            id_: int = 0
    ):
        super().__init__()
        self._id = id_

    # id
    def set_id(self, id_: int) -> None:
        self._id = id_

    def get_id(self) -> int:
        return self._id

    # Printable
    def to_id(self) -> str:
        return f'{self.get_id()}'


class BaseEdge(tp.Generic[Node], Printable):

    def __init__(
            self,
            nodes: tp.Optional[tp.List[Node]] = None
    ):
        super().__init__()
        if nodes is None:
            nodes = []
        self._nodes: tp.List[Node] = nodes

    # nodes
    def add_node(self, node: Node) -> None:
        assert node not in self._nodes, f'{node.to_unique()} already present in {self.to_unique()}.'
        self._nodes.append(node)

    # def set_node(self, index: int, node: Node):
    #     assert 0 <= index < len(self._nodes), f'Index {index} out of bounds.'
    #     assert node not in self._nodes[:index] + self._nodes[index + 1:], f'{node.to_unique()} doubly present.'
    #     self._nodes[index] = node

    def get_nodes(self) -> tp.List[Node]:
        return self._nodes

    def get_node(self, index: int) -> Node:
        assert 0 <= index < len(self._nodes), f'Index {index} out of bounds.'
        return self._nodes[index]

    def get_node_ids(self) -> tp.List[int]:
        return [node.get_id() for node in self.get_nodes()]

    # Printable
    def to_id(self) -> str:
        return '-'.join([f'{id_}' for id_ in self.get_node_ids()])
