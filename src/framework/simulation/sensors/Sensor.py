import typing as tp
from abc import abstractmethod

import numpy as np
from numpy.random.mtrand import RandomState

from src.framework.graph.data import SubData
from src.framework.graph.data.DataFactory import DataFactory
from src.framework.graph.types.scslam2d.edges.CalibratingEdge import SubCalibratingEdge
from src.framework.graph.types.scslam2d.nodes.information.InformationNode import SubInformationNode
from src.framework.graph.types.scslam2d.nodes.parameter.ParameterNode import SubParameterNode
from src.framework.math.matrix.square import SubSquare, SquareFactory
from src.framework.math.matrix.vector import SubVector, VectorFactory

T = tp.TypeVar('T')
SubSensor = tp.TypeVar('SubSensor', bound='Sensor')


class Sensor(tp.Generic[T]):

    _rng: np.random.RandomState
    _type: tp.Type[T]

    def __init__(
            self,
            seed: tp.Optional[int] = None,
            info_matrix: tp.Optional[SubSquare] = None
    ):
        self.set_seed(seed)

        # information
        if info_matrix is None:
            info_matrix = SquareFactory.from_dim(self.get_dimension()).identity()
        self._info_matrix: SubSquare = info_matrix

        # parameter
        self._parameters: tp.List[SubParameterNode] = []
        self._info_node: tp.Optional[SubInformationNode] = None

    # measurement-type
    @classmethod
    def get_dimension(cls):
        return DataFactory.from_type(cls.get_type()).get_dim()

    @classmethod
    def get_type(cls) -> tp.Type[SubData]:
        return cls._type

    # parameter
    def add_parameter(
            self,
            parameter: SubParameterNode
    ) -> None:
        self._parameters.append(parameter)

    def get_parameters(self) -> tp.List[SubParameterNode]:
        return self._parameters

    # information
    def add_info_node(
            self,
            node: SubInformationNode
    ) -> None:
        assert self.get_dimension() == node.get_dimension()
        self._info_node = node
        # self._matrix = SquareFactory.from_dim(self.get_dimension()).identity()

    def get_info_node(self) -> SubInformationNode:
        assert self.has_info_node()
        return self._info_node

    def has_info_node(self) -> bool:
        return self._info_node is not None

    def set_info_matrix(self, info_matrix: SubSquare) -> None:
        self._info_matrix = info_matrix

    def get_information(self) -> SubSquare:
        if self.has_info_node():
            return self._info_node.get_matrix()
        return self._info_matrix

    # noise
    def set_seed(self, seed: tp.Optional[int] = None):
        self._rng = np.random.RandomState(seed)

    def generate_noise(self) -> SubVector:
        dim: int = self.get_dimension()
        vector_type: tp.Type[SubVector] = VectorFactory.from_dim(dim)
        return vector_type(
            self._rng.multivariate_normal(
                mean=[0] * dim,
                cov=self.get_information().inverse().array()
            )
        )

    @abstractmethod
    def measure(self, value: T) -> T:
        """ Adds noise to the value. """
        pass

    @abstractmethod
    def compose(self, value: T) -> T:
        """ Composes the value by sequentially adding all stored parameters. """
        pass

    @abstractmethod
    def decompose(self, value: T) -> T:
        """ Decomposes the value by, in reverse order, subtracting all stored parameters. """
        pass

    def extend_edge(
            self,
            edge: SubCalibratingEdge
    ) -> SubCalibratingEdge:
        assert edge.get_type() == self.get_type()

        # add parameters
        for parameter in self._parameters:
            edge.add_parameter(parameter)

        # add information
        edge.set_info_matrix(self._info_matrix)
        if self.has_info_node():
            edge.add_info_node(self._info_node)

        return edge
