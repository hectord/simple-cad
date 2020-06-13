# -*- coding: utf-8 -*-


class Variable:

    def __init__(self,
                 solver: 'Solver',
                 identifier: int):
        self._solver = solver
        self._identifier = identifier

    @property
    def is_constrained(self) -> bool:
        return self in self._solver.constrained_variables()

    @property
    def identifier(self) -> int:
        return self._identifier

    def __hash__(self):
        return hash(self._identifier)

    def __eq__(self, other: 'Variable'):
        return (self._solver is other._solver and
                self._identifier == other._identifier)

    def __str__(self) -> str:
        return 'v{}'.format(self._identifier)
