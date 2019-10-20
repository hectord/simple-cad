"""
Graphical elements added in a sketch
"""

from typing import Tuple
from solver import Variable


class GeometricElement:

    @property
    def is_constrained(self) -> bool:
        raise NotImplementedError


class Point(GeometricElement):

    def __init__(self, variables: Tuple[Variable, Variable, Variable]):
        self._variables = variables

    @property
    def is_constrained(self) -> bool:
        for variable in self._variables:
            if not variable.is_constrained:
                return False

        return True

    def __getitem__(self, i: int):
        return self._variables[i]


class Line(GeometricElement):

    def __init__(self,
                 point: Point,
                 diffs: Tuple[Variable, Variable, Variable]):
        self._point = point
        self._diffs = diffs

    @property
    def point(self) -> Point:
        return self._point

    @property
    def is_constrained(self) -> bool:

        if not self._point.is_constrained:
            return False

        return all(lambda x: x.is_constrained, self._diffs)
