
import operator
from typing import Callable


class Vector:
    """
    A vector in the 3D space
    """

    def __init__(self, position):
        self._position = position

    @property
    def length(self) -> float:
        square_sum = sum([x**2 for x in self._position])

        return square_sum**0.5

    def __mul__(self, other: 'Vector') -> float:
        return sum(self._fuse(self, other, operator.mul)._position)

    @property
    def size(self) -> int:
        return len(self._position)

    def __getitem__(self, i: int) -> float:
        return self._position[i]

    def _fuse(self,
              vect1: 'Vector',
              vect2: 'Vector',
              operation: Callable[[float, float], float]):
        assert vect1.size == vect2.size

        pose = []

        for dimension in range(vect1.size):
            pose.append(operation(vect1[dimension], vect2[dimension]))

        return Vector(tuple(pose))

    def __add__(self, other: 'Vector'):
        return self._fuse(self, other, operator.add)

    def __sub__(self, other: 'Vector'):
        return self._fuse(self, other, operator.sub)

    def __str__(self):
        position = ', '.join(map(str, self._position))

        return f'v[{position}]'
