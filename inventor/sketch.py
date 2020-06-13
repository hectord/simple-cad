
from typing import Tuple

from solver.solver import Solver
from solver.rule import Rule
from geometric_elements import Point, Line


class Sketch:

    def __init__(self):
        self._solver = Solver()
        self._geometric_elements = []

    @property
    def solver(self) -> Solver:
        return self._solver

    @property
    def is_constrained(self) -> bool:
        return all([x.is_constrained for x in self._geometric_elements])

    def add_variable_point(self) -> Point:
        coordinates = [self._solver.add_variable() for i in range(3)]

        point = Point(tuple(coordinates))
        self._geometric_elements.append(point)
        return point

    def add_variable_line(self):
        point = self.add_variable_point()

        diffs = [self._solver.add_variable() for i in range(3)]

        line = Line(point, diffs)
        self._geometric_elements.append(line)
        return line

    def add_point(self, positions: Tuple[float, float, float]):
        coordinates = []

        for position in positions:
            new_constant = self._solver.add_variable()
            self._solver.add_rule(Rule(new_constant, [], position))

            coordinates.append(new_constant)

        point = Point(tuple(coordinates))
        self._geometric_elements.append(point)
        return point

    def add_line(self,
                 positions: Tuple[float, float, float],
                 diffs: Tuple[float, float, float]):

        point = self.add_point(positions)
        diff_list = []

        for diff in diffs:
            new_constant = self._solver.add_variable()
            self._solver.add_rule(Rule(new_constant, [], diff))

            diff_list.append(new_constant)

        return Line(point, diff_list)

    def add_alignment_constraint(self,
                                 point1: Point,
                                 point2: Point,
                                 dimension: int,
                                 distance: float):

        new_rule = Rule(point1[dimension],
                        [(1, point2[dimension])],
                        distance)

        self._solver.add_rule(new_rule)
