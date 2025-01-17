import typing as tp

from src.framework.graph.data.Data import Data
from src.framework.graph.data.Parser import Parser
from src.framework.math.matrix.square import SubSquare, Square3, Square2
from src.framework.math.matrix.vector import SubVector
from src.framework.math.matrix.vector import VectorFactory

SubDataSymmetric = tp.TypeVar('SubDataSymmetric', bound='DataSquare', covariant=True)


class DataSymmetric(Data[SubSquare]):
    _type: tp.Type[SubSquare]

    def __init__(
            self,
            value: tp.Optional[SubSquare] = None
    ):
        super().__init__(value)
        self._size = self._type.dim()

    def to_vector(self) -> SubVector:
        return VectorFactory.from_dim(self.dim())(
            Parser.symmetric_to_list(self.get_value())
        )

    def set_from_vector(self, vector: SubVector) -> None:
        assert vector.dim() == self.dim()
        self.set_value(Parser.list_to_symmetric(vector.to_list()))

    def read(self, words: tp.List[str]) -> None:
        floats: tp.List[float] = Parser.words_to_list(words)
        value: SubSquare = Parser.list_to_symmetric(floats)
        self.set_value(value)

    def write(self) -> tp.List[str]:
        floats: tp.List[float] = Parser.symmetric_to_list(self.get_value())
        return Parser.list_to_words(floats)

    def oplus(self, delta: SubVector) -> SubSquare:
        assert self.has_value()
        assert delta.dim() == self.dim()
        symmetric: SubSquare = Parser.list_to_symmetric(delta.to_list())
        return self._type(self.get_value().array() + symmetric.array())

    @classmethod
    def dim(cls) -> int:
        dim: int = cls._type.dim()
        return int((dim + 1) * dim / 2)


class DataSymmetric2(DataSymmetric):
    _type = Square2


class DataSymmetric3(DataSymmetric):
    _type = Square3
