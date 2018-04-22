#!/usr/bin/python3

# Authors: Jared Bass, Dan Salerno, Brian Silverman
# We pledge our honor that we have abided by the Stevens Honor System
#   - Jared Bass
#   - Dan Salerno
#   - Brian Silverman

import grid

EXAMPLE_SOLUTION = grid.Grid((
        4, 8, 3, 9, 2, 1, 6, 5, 7,
        9, 6, 7, 3, 4, 5, 8, 2, 1,
        2, 5, 1, 8, 7, 6, 4, 9, 3,
        5, 4, 8, 1, 3, 2, 9, 7, 6,
        7, 2, 9, 5, 6, 4, 1, 3, 8,
        1, 3, 6, 7, 9, 8, 2, 4, 5,
        3, 7, 2, 6, 8, 9, 5, 1, 4,
        8, 1, 4, 2, 5, 3, 7, 6, 9,
        6, 9, 5, 4, 1, 7, 3, 8, 2,
))
"""The solution to the first grid from the problem."""

def main():
    # hardcoding the file_name because im lazy
    file_name = "p096_sudoku.txt"
    grids = []

    # read the file
    grid_values = None
    grids = []
    with open(file_name) as f:
        for line in f:
            if line.startswith("Grid"):
                # Time to finish the current one and start a new one.
                if grid_values is not None:
                    grids.append(grid.Grid(grid_values))
                grid_values = []
            else:
                # For each character in the line, convert it to an int, or
                # use None instead if it's 0.
                grid_values.extend(
                        (int(c) if c != '0' else None for c in line.strip()))
    # Make sure to grab the last grid.
    grids.append(grid.Grid(grid_values))
    assert len(grids) == 50

    print(str(grids[0]))
    print(grids[0].pretty())
    print(EXAMPLE_SOLUTION.pretty())
    assert EXAMPLE_SOLUTION.is_complete() and EXAMPLE_SOLUTION.is_valid()

    # Some basic sanity checking.
    for g in grids:
        assert not g.is_complete(), '%s is already finished' % (g,)
        assert g.is_valid(), '%s is impossible' % (g,)

if __name__ == "__main__":
    main()
