import numpy as np
from abc import ABC, abstractmethod

from src.framework.structures import *
from src.framework.groups.Group import Group
from src.framework.groups.SO import SO


class SE(Group, ABC):

    # constructor
    def __init__(self, translation, rotation):
        assert isinstance(translation, Vector)
        assert isinstance(rotation, SO)
        self._translation = translation
        self._rotation = rotation

    # public methods
    def translation(self):
        return self._translation

    def rotation(self):
        return self._rotation

    def vector(self):
        rotation = self.rotation()
        translation = self.translation()
        rotation_vector = rotation.vector()
        inverse_jacobian = rotation.inverse_jacobian()
        translation_vector = Vector(inverse_jacobian @ translation)
        vector = Vector(np.vstack((translation_vector, rotation_vector)))
        return vector

    def plus(self, vector):
        assert isinstance(vector, Vector)
        increment = type(self).from_vector(vector)
        return self * increment

    def minus(self, transformation):
        assert isinstance(transformation, SE)
        difference = transformation.inverse() * self
        return difference.vector()

    # public class-methods
    @classmethod
    def from_vectors(cls, translation_vector, rotation_vector):
        assert isinstance(translation_vector, Vector)
        assert isinstance(rotation_vector, Vector)
        rotation = cls._rotation_type.from_vector(rotation_vector)
        jacobian = rotation.jacobian()
        translation = Vector(jacobian @ translation_vector)
        return cls(translation, rotation)

    # private class-methods
    @classmethod
    def _construct_matrix(cls, translation, rotation):
        assert isinstance(translation, Vector)
        assert isinstance(rotation, SO)
        rotation_matrix = rotation.matrix()
        pad = np.zeros((1, cls._dim))
        matrix = np.block([[rotation_matrix, translation],
                           [pad, 1]])
        return Square(matrix)

    @classmethod
    def _extract_translation(cls, matrix):
        assert isinstance(matrix, Square)
        translation = Vector(matrix[: cls._dim, cls._dim:])
        return translation

    @classmethod
    def _extract_rotation(cls, matrix):
        assert isinstance(matrix, Square)
        matrix = Square(matrix[: cls._dim, : cls._dim])
        rotation = cls._rotation_type.from_matrix(matrix)
        return rotation

    # abstract properties
    @property
    @classmethod
    @abstractmethod
    def _rotation_type(cls) -> SO:
        pass

    # abstract implementations
    def matrix(self):
        return self._construct_matrix(self._translation, self._rotation)

    def inverse(self):
        translation = self.translation()
        rotation = self.rotation()
        inverse_rotation = rotation.inverse()
        inverse_translation = - inverse_rotation * translation
        return type(self)(inverse_translation, inverse_rotation)

    @classmethod
    def from_matrix(cls, matrix):
        assert isinstance(matrix, Square)
        translation = cls._extract_translation(matrix)
        rotation = cls._extract_rotation(matrix)
        return cls(translation, rotation)

    @classmethod
    def from_vector(cls, vector):
        assert isinstance(vector, Vector)
        translation_vector = vector[0: cls._dim]
        rotation_vector = vector[cls._dim:]
        return cls.from_vectors(translation_vector, rotation_vector)
