"""
Keep constraints in sync
"""

from typing import List, Tuple, Set, Dict


class InvalidConstraint(Exception):
    pass


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
