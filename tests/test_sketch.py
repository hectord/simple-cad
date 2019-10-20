
import unittest

from sketch import Sketch
from solver import InvalidConstraint


class TestSketchBuilder(unittest.TestCase):

    def test_sketch_one_point_variable(self):
        sketch = Sketch()

        sketch.add_point((0.0, 0.0, 0.0))
        sketch.add_variable_point()
        self.assertFalse(sketch.is_constrained)

    def test_sketch_one_point_constant(self):
        sketch = Sketch()

        sketch.add_point((0.0, 0.0, 0.0))
        self.assertTrue(sketch.is_constrained)

    def test_simple_sketch(self):

        sketch = Sketch()

        var1 = sketch.add_variable_point()
        var2 = sketch.add_point((2.0, 3.0, 4.0))

        # make the points align
        sketch.add_alignment_constraint(var1, var2, 0, 0.0)
        sketch.add_alignment_constraint(var1, var2, 1, 0.0)
        sketch.add_alignment_constraint(var1, var2, 2, 0.0)

        self.assertTrue(sketch.is_constrained)

    def test_wrong_constraints(self):

        sketch = Sketch()

        var1 = sketch.add_point((2.0, 4.1, 5.1))
        var2 = sketch.add_point((2.0, 3.0, 4.0))

        sketch.add_alignment_constraint(var1, var2, 0, 0.0)

        with self.assertRaises(InvalidConstraint):
            sketch.add_alignment_constraint(var1, var2, 1, 0.0)

    def test_shifted_sketch(self):

        sketch = Sketch()

        var1 = sketch.add_variable_point()
        var2 = sketch.add_point((2.0, 3.0, 4.0))

        sketch.add_alignment_constraint(var1, var2, 0, 2.0)
        sketch.add_alignment_constraint(var1, var2, 1, 3.0)
        sketch.add_alignment_constraint(var1, var2, 2, 4.0)

        self.assertTrue(sketch.is_constrained)


if __name__ == '__main__':
    unittest.main(verbosity=3)
