from typing import *

import numpy as np

from src.framework.structures import Square


class Parser(object):

    # helper-methods
    @staticmethod
    def array_to_list(array: np.ndarray) -> List[float]:
        return list(array.flatten())

    @staticmethod
    def list_to_string(elements: List[float]) -> str:
        elements = [float('{:.5e}'.format(element)) for element in elements]
        for i, element in enumerate(elements):
            if element.is_integer():
                elements[i] = int(element)
        return ' '.join(str(element) for element in elements)
        # return ' '.join([str(float('{:.5e}'.format(element))) for element in elements])

    @classmethod
    def symmetric_to_list(cls, matrix: Square) -> List[float]:
        elements = []
        indices = np.arange(matrix.shape[0])
        for i in indices:
            for j in indices[i:]:
                elements.append(matrix[i][j])
        return elements

    @classmethod
    def list_to_symmetric(cls, elements: List[float]) -> Square:
        length = len(elements)
        dimension = -0.5 + 0.5 * np.sqrt(1 + 8 * length)
        assert dimension.is_integer(), \
            'elements {} are not divisible to form a symmetric matrix ({})'.format(elements, dimension)
        dimension = int(dimension)
        matrix = Square.zeros(dimension)
        indices = np.arange(dimension)
        count = 0
        for i in indices:
            for j in indices[i:]:
                matrix[i, j] = elements[count]
                matrix[j, i] = matrix[i, j]
                count += 1
        return matrix
