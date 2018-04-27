#!/usr/bin/python3

# Authors: Jared Bass, Dan Salerno, Brian Silverman
# We pledge our honor that we have abided by the Stevens Honor System
#   - Jared Bass
#   - Dan Salerno
#   - Brian Silverman

import solver
import grid
import unittest

from grid_test import TEST_VALUES

class TestPossibilities(unittest.TestCase):
    def test_complete(self):
        g = grid.Grid(TEST_VALUES)
        self.assertEqual(grid.GridStorage([None] * 81), solver.possibilities(g))

    def test_single_cell(self):
        """Tests removing each individual cell."""
        for i in range(81):
            values = list(TEST_VALUES)
            p = [None] * 81
            p[i] = set([values[i]])
            values[i] = None

            g = grid.Grid(values)
            self.assertEqual(grid.GridStorage(p), solver.possibilities(g))
            self.assertEqual(grid.Grid(TEST_VALUES), solver.set_trivial(g))

    def test_row(self):
        """Tests removing a whole row of values.

        The column of each should still fix the value."""
        values = list(TEST_VALUES)
        p = [None] * 81
        for i in range(9, 18):
            p[i] = set([values[i]])
            values[i] = None

        g = grid.Grid(values)
        self.assertEqual(grid.GridStorage(p), solver.possibilities(g))
        self.assertEqual(grid.Grid(TEST_VALUES), solver.set_trivial(g))

    def test_two_rows(self):
        """Tests removing two rows of value, within the same row of squares.

        This means the possibilities are mix-and-matching the values from each
        row."""
        values = list(TEST_VALUES)
        p = [None] * 81
        for i in range(9, 18):
            possible = set([values[i], values[i + 9]])
            p[i] = possible
            p[i + 9] = possible
            values[i] = None
            values[i + 9] = None

        g = grid.Grid(values)
        self.assertEqual(grid.GridStorage(p), solver.possibilities(g))

if __name__ == "__main__":
    unittest.main()
