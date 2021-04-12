import typing as tp
from abc import abstractmethod

from src.framework.graph.BaseGraph import BaseGraph, BaseNode, BaseEdge
from src.framework.graph.protocols.ReadWrite import ReadWrite
from src.framework.math.matrix.square import SubSquare
from src.framework.math.matrix.vector import SubVector

SubNode = tp.TypeVar('SubNode', bound='FactorNode')
SubEdge = tp.TypeVar('SubEdge', bound='FactorEdge')
SubElement = tp.Union[SubNode, SubEdge]


class FactorGraph(BaseGraph):

    # error
    def compute_error(self) -> float:
        error: float = 0
        for edge in self.get_edges():
            error += edge.compute_error()
        return error


T = tp.TypeVar('T')


class FactorNode(tp.Generic[T], BaseNode, ReadWrite):

    def __init__(
            self,
            id_: int = 0
    ):
        super().__init__(id_)
        self._is_fixed = False

    def fix(self, is_fixed: bool = True) -> None:
        self._is_fixed = is_fixed

    def is_fixed(self) -> bool:
        return self._is_fixed

    # value
    @abstractmethod
    def get_value(self) -> T:
        pass


class FactorEdge(tp.Generic[T], BaseEdge, ReadWrite):

    @abstractmethod
    def get_cardinality(self) -> int:
        pass

    # measurement
    @abstractmethod
    def get_measurement(self) -> T:
        """ Returns the (externally assigned) measurement encoded in the edge. """
        pass

    # estimate
    @abstractmethod
    def get_estimate(self) -> T:
        """ Returns an estimate of the measurement. """
        pass

    # information
    @abstractmethod
    def get_information(self) -> SubSquare:
        pass

    # error
    @abstractmethod
    def compute_error_vector(self) -> SubVector:
        pass

    def compute_error(self) -> float:
        error_vector: SubVector = self.compute_error_vector()
        return self.mahalanobis_distance(error_vector, self.get_information())

    # helper methods
    @staticmethod
    def mahalanobis_distance(
            vector: SubVector,
            information: SubSquare
    ) -> float:
        assert vector.get_dimension() == information.get_dimension(), f'{vector} and {information} are not of appropriate dimensions.'
        return float(vector.array().transpose() @ information.inverse().array() @ vector.array())