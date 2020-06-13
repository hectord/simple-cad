
import unittest

from solver.solver import Solver
from solver.rule import Rule


class TestSolver(unittest.TestCase):

    def test_simple_constrained_problem(self):
        solver = Solver()

        var1 = solver.add_variable()
        var2 = solver.add_variable()

        solver.add_rule(Rule(var1, [(1, var2)], 3))
        solver.add_rule(Rule(var2, [], 3))

        self.assertTrue(solver.is_constrained)

    def test_unconstrained_problem(self):
        solver = Solver()

        var1 = solver.add_variable()
        var2 = solver.add_variable()

        solver.add_rule(Rule(var1, [(1, var2)], 3))

        self.assertFalse(solver.is_constrained)


if __name__ == '__main__':
    unittest.main(verbosity=3)
