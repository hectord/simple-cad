
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

    def _fuse(self,
              v1: 'Vector',
              v2: 'Vector',
              operator: Callable[[float, float], float]):

        pose = [operator(x, y) for (x, y) in zip(v1._position, v2._position)]

        return Vector(tuple(pose))

    def __add__(self, other: 'Vector'):
        return self._fuse(self, other, operator.add)

    def __sub__(self, other: 'Vector'):
        return self._fuse(self, other, operator.sub)

    def __str__(self):
        position = ', '.join(map(str, self._position))

        return f'v[{position}]'

