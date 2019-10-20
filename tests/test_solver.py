
import unittest

from solver import Solver, Rule


class TestSolver(unittest.TestCase):

    def test_simple_constrained_problem(self):
        s = Solver()

        var1 = s.add_variable()
        var2 = s.add_variable()

        s.add_rule(Rule(var1, [(1, var2)], 3))
        s.add_rule(Rule(var2, [], 3))

        self.assertTrue(s.is_constrained)

    def test_unconstrained_problem(self):
        s = Solver()

        var1 = s.add_variable()
        var2 = s.add_variable()

        s.add_rule(Rule(var1, [(1, var2)], 3))

        self.assertFalse(s.is_constrained)


if __name__ == '__main__':
    unittest.main(verbosity=3)
