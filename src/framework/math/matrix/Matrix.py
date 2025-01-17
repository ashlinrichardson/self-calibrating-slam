import copy
import typing as tp
from abc import abstractmethod

import numpy as np

SubMatrix = tp.TypeVar('SubMatrix', bound='Matrix', covariant=True)
List2D = tp.List[tp.List[tp.Union[tp.Any]]]


class Matrix(object):

    _matrix: np.ndarray

    def __init__(
            self,
            data: tp.Union[List2D, np.ndarray]
    ):
        super().__init__()
        self._matrix = np.asarray(data).astype(float)

    # alternative representations
    def array(self) -> np.ndarray:
        return self._matrix

    # operators
    def __iadd__(self, other: SubMatrix) -> None:
        assert other.shape() == self.shape()
        self._matrix += other.array()

    def __add__(self, other: SubMatrix) -> SubMatrix:
        return type(self)(self.array() + other.array())

    # access
    def __getitem__(self, item):
        return self._matrix[item]

    def __setitem__(self, key, value: float) -> None:
        self._matrix[key] = value

    # properties
    def shape(self) -> tp.Tuple[int, int]:
        return self._matrix.shape

    def is_zero(self) -> bool:
        return not self._matrix.any()

    # print
    def to_string(
            self,
            precision: tp.Optional[int] = None,
            suppress_small: bool = False
    ) -> str:
        return np.array2string(
            self.array(), precision=precision, suppress_small=suppress_small,
            max_line_width=200, edgeitems=5
        )

    def __str__(self):
        return self.to_string(
            precision=3,
            suppress_small=True
        )

    def __repr__(self):
        name: str = self.__class__.__name__
        return name + np.array2string(
            self.array(),
            prefix=name
        )
