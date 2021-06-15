import typing as tp

SubMultiDimensional = tp.TypeVar('SubMultiDimensional', bound='MultiDimensional')


class Dimensional(object):
    _dim: int

    @classmethod
    def get_dim(cls) -> int:
        return cls._dim
