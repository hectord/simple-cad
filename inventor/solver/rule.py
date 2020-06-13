# -*- coding: utf-8 -*-

from typing import List, Tuple, Set, Dict

from solver.variable import Variable


class Rule:

    def __init__(self,
                 base: Variable,
                 mults: List[Tuple[float, Variable]],
                 constant: float):
        self._base = base
        self._mults = mults
        self._constant = constant

    @property
    def base(self) -> Variable:
        return self._base

    def __str__(self) -> str:
        ret = []

        for coeff, variable in self._mults:
            if coeff == 1.0:
                ret.append('%s' % variable)
            else:
                ret.append('%.2f*%s' % (coeff, variable))

        if not ret or self._constant != 0.0:
            ret.append('%.d' % self._constant)

        return str(self.base) + '=' + '+'.join(ret)

    def eval(self, values: Dict[Variable, float]):
        assert self.is_set_with(values)

        ret = self._constant

        for coeff, variable in self._mults:
            ret += coeff * values[variable]
        return ret

    def is_set_with(self, variables: Set[Variable]):

        for _, variable in self._mults:
            if variable not in variables:
                return False

        return True

    def uses(self, other_variable: Variable) -> bool:

        for _, variable in self._mults:
            if other_variable == variable:
                return True
        return False
