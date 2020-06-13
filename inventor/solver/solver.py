# -*- coding: utf-8 -*-
"""
Keep constraints in sync
"""

from typing import List, Dict

from solver.rule import Rule
from solver.variable import Variable


class InvalidConstraint(Exception):
    pass


class Solver:

    def __init__(self):
        self._next_identifier = 1
        # the variables we know their values (None
        #  if not available)
        self._rules = []
        self._variables = set()

    def constrained_variables_with(self, new_rules: List[Rule]) -> Dict[Variable, float]:
        variables_set = {}
        validated_rules = set()
        assignment_found = True

        rules = self._rules.copy()
        rules.extend(new_rules)

        while assignment_found:

            assignment_found = False

            for rule in rules:

                if rule in validated_rules:
                    continue

                if rule.is_set_with(variables_set):
                    new_val = rule.eval(variables_set)

                    if rule.base in variables_set:
                        if new_val != variables_set[rule.base]:
                            raise InvalidConstraint()
                    variables_set[rule.base] = new_val
                    assignment_found = True

                    validated_rules.add(rule)
                    break

        return variables_set

    def constrained_variables(self) -> Dict[Variable, float]:
        return self.constrained_variables_with([])

    @property
    def is_constrained(self) -> bool:

        return len(self.constrained_variables()) == len(self._rules)

    def __str__(self) -> str:
        variables = []

        for rule in self._rules:
            variables.append(str(rule))

        return '({})'.format(','.join(variables))

    def add_variable(self) -> Variable:
        new_variable = Variable(self, self._next_identifier)
        self._variables.add(new_variable)
        self._next_identifier += 1
        return new_variable

    def add_rule(self, rule: Rule):
        self.constrained_variables_with([rule])
        self._rules.append(rule)
