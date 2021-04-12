import typing as tp

from src.framework.graph.Database import Database
from src.framework.graph.types.scslam2d.edges.CalibratingEdge import CalibratingEdge, SubCalibratingEdge
from src.framework.graph.types.scslam2d.nodes.CalibratingNode import CalibratingNode, SubCalibratingNode
from src.framework.graph.types.scslam2d.nodes.information.InformationNode import SubInformationNode
from src.framework.graph.types.scslam2d.nodes.parameter.ParameterNode import SubParameterNode
from src.utils.TwoWayDict import TwoWayDict

Element = tp.Union[SubCalibratingNode, SubCalibratingEdge]


class SuffixDatabase(Database):

    def __init__(self):
        self._elements = TwoWayDict()
        self._parameters = TwoWayDict()
        self._informations = TwoWayDict()

    # register
    def register_type(
            self,
            tag: str,
            type_: tp.Type[Element]
    ) -> None:
        self._elements[type_] = tag

    def register_parameter_suffix(
            self,
            suffix: str,
            type_: tp.Type[SubParameterNode]
    ) -> None:
        self._parameters[suffix] = type_

    def register_information_suffix(
            self,
            suffix: str,
            type_: tp.Type[SubInformationNode]
    ) -> None:
        self._informations[suffix] = type_

    # tag to element
    def from_tag(self, tag: str) -> Element:
        words: tp.List[str] = tag.split('_')
        suffixes: tp.List[str] = []
        for word in words[::-1]:
            if word in self._parameters or word in self._informations:
                suffixes.append(word)
            else:
                tag = '_'.join(words[: 1 + words.index(word)])
                break
        assert tag in self._elements, f"Tag '{tag}' not found in database."
        suffixes = suffixes[::-1]
        element: Element = self._elements[tag]()

        # if element is a node
        if isinstance(element, CalibratingNode):
            assert not suffixes, f"'{suffixes}' are unprocessed."

        # if element is an edge
        elif isinstance(element, CalibratingEdge):
            count: int = 0
            for suffix in suffixes:
                assert suffix in self._parameters or suffix in self._informations, f"'{suffix}' is not found."
                count += 1
            element.set_num_additional(count)
        return element

    def contains_tag(self, tag: str) -> bool:
        return tag in self._elements

    def from_element(self, element: Element) -> str:
        tag: str = self._elements[type(element)]

        # if element is a node
        if isinstance(element, CalibratingNode):
            return f"{tag}"

        # if element is an edge
        elif isinstance(element, CalibratingEdge):
            suffixes: tp.List[str] = []
            parameter: SubParameterNode
            for parameter in element.get_parameters():
                type_: tp.Type[SubParameterNode] = type(parameter)
                assert type_ in self._parameters
                suffixes.append(self._parameters[type_])
            if element.has_info_node():
                information: SubInformationNode = element.get_info_node()
                type_: tp.Type[SubInformationNode] = type(information)
                assert type_ in self._informations
                suffixes.append(self._informations[type_])
            return '_'.join([tag] + suffixes)

    def contains_element(self, type_: tp.Type[Element]) -> bool:
        return type_ in self._elements