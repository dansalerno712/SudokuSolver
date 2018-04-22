#!/usr/bin/python3

# Authors: Jared Bass, Dan Salerno, Brian Silverman
# We pledge our honor that we have abided by the Stevens Honor System
#   - Jared Bass
#   - Dan Salerno
#   - Brian Silverman

import grid
import unittest

TEST_VALUES = (
        1, 2, 3, 4, 5, 6, 7, 8, 9,
        4, 5, 6, 7, 8, 9, 1, 2, 3,
        7, 8, 9, 1, 2, 3, 4, 5, 6,
        2, 3, 4, 5, 6, 7, 8, 9, 1,
        5, 6, 7, 8, 9, 1, 2, 3, 4,
        8, 9, 1, 2, 3, 4, 5, 6, 7,
        3, 4, 5, 6, 7, 8, 9, 1, 2,
        6, 7, 8, 9, 1, 2, 3, 4, 5,
        9, 1, 2, 3, 4, 5, 6, 7, 8,
)
"""A (trivial) solved grid."""

class TestGrid(unittest.TestCase):
    def test_constructor(self):
        grid.Grid(TEST_VALUES)

        with self.assertRaisesRegex(AssertionError, "invalid length"):
            grid.Grid(TEST_VALUES[:-2])
        with self.assertRaisesRegex(AssertionError, "invalid length"):
            grid.Grid(TEST_VALUES[1:])
        with self.assertRaisesRegex(AssertionError, "invalid length"):
            grid.Grid(TEST_VALUES + (1,))

        with self.assertRaisesRegex(AssertionError, "invalid value"):
            values = list(TEST_VALUES)
            values[5] = 0
            grid.Grid(values)
        with self.assertRaisesRegex(AssertionError, "invalid value"):
            values = list(TEST_VALUES)
            values[5] = -100
            grid.Grid(values)

        with self.assertRaisesRegex(AssertionError, "invalid value"):
            values = list(TEST_VALUES)
            values[5] = 10
            grid.Grid(values)
        with self.assertRaisesRegex(AssertionError, "invalid value"):
            values = list(TEST_VALUES)
            values[5] = 100
            grid.Grid(values)

        values = list(TEST_VALUES)
        values[5] = None
        grid.Grid(values)

        grid.Grid([None] * len(TEST_VALUES))

        values = [None] * len(TEST_VALUES)
        values[6] = 3
        grid.Grid(values)

    def test_cell(self):
        g = grid.Grid(TEST_VALUES)
        self.assertEqual(g.cell(2, 4), 2)
        self.assertEqual(g.cell(4, 2), 7)
        self.assertEqual(g.cell(8, 8), 8)

    def test_square(self):
        g = grid.Grid(TEST_VALUES)
        self.assertEqual(g.square(0), (1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(g.square(1), (4, 5, 6, 7, 8, 9, 1, 2, 3))
        self.assertEqual(g.square(3), (2, 3, 4, 5, 6, 7, 8, 9, 1))
        self.assertEqual(g.square(8), (9, 1, 2, 3, 4, 5, 6, 7, 8))
        self.assertEqual(g.square(7), (6, 7, 8, 9, 1, 2, 3, 4, 5))

    def test_row(self):
        g = grid.Grid(TEST_VALUES)
        self.assertEqual(g.row(0), (1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertEqual(g.row(7), (6, 7, 8, 9, 1, 2, 3, 4, 5))
        self.assertEqual(g.row(8), (9, 1, 2, 3, 4, 5, 6, 7, 8))

    def test_column(self):
        g = grid.Grid(TEST_VALUES)
        self.assertEqual(g.column(0), (1, 4, 7, 2, 5, 8, 3, 6, 9))
        self.assertEqual(g.column(1), (2, 5, 8, 3, 6, 9, 4, 7, 1))
        self.assertEqual(g.column(7), (8, 2, 5, 9, 3, 6, 1, 4, 7))
        self.assertEqual(g.column(8), (9, 3, 6, 1, 4, 7, 2, 5, 8))

    def test_is_complete(self):
        self.assertTrue(grid.Grid(TEST_VALUES).is_complete())

        values = list(TEST_VALUES)
        values[5] = 9
        self.assertTrue(grid.Grid(values).is_complete())

        values = list(TEST_VALUES)
        values[5] = None
        self.assertFalse(grid.Grid(values).is_complete())

        self.assertFalse(grid.Grid([None] * len(TEST_VALUES)).is_complete())

        values = [None] * len(TEST_VALUES)
        values[6] = 3
        self.assertFalse(grid.Grid(values).is_complete())

    def test_is_valid(self):
        self.assertTrue(grid.Grid(TEST_VALUES).is_valid())

        values = list(TEST_VALUES)
        values[5] = 9
        self.assertFalse(grid.Grid(values).is_valid())

        values = list(TEST_VALUES)
        values[5] = None
        self.assertTrue(grid.Grid(values).is_valid())

        self.assertTrue(grid.Grid([None] * len(TEST_VALUES)).is_valid())

        values = [None] * len(TEST_VALUES)
        values[6] = 3
        self.assertTrue(grid.Grid(values).is_valid())

    def test_pretty(self):
        expected = \
'''+-------+-------+-------+
| 1 2 3 | 4 5 6 | 7 8 9 |
| 4 5 6 | 7 8 9 | 1 2 3 |
| 7 8 9 | 1 2 3 | 4 5 6 |
+-------+-------+-------+
| 2 3 4 | 5 6 7 | 8 9 1 |
| 5 6 7 | 8 9 1 | 2 3 4 |
| 8 9 1 | 2 3 4 | 5 6 7 |
+-------+-------+-------+
| 3 4 5 | 6 7 8 | 9 1 2 |
| 6 7 8 | 9 1 2 | 3 4 5 |
| 9 1 2 | 3 4 5 | 6 7 8 |
+-------+-------+-------+'''
        self.assertEqual(expected, grid.Grid(TEST_VALUES).pretty())

        values = list(TEST_VALUES)
        values[0] = None
        expected = list(expected)
        expected[28] = 'x'
        expected = ''.join(expected)
        self.assertTrue(grid.Grid(values).is_valid())
        self.assertEqual(expected, grid.Grid(values).pretty())

if __name__ == "__main__":
    unittest.main()
