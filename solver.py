#!/usr/bin/python3

# Authors: Jared Bass, Dan Salerno, Brian Silverman
# We pledge our honor that we have abided by the Stevens Honor System
#   - Jared Bass
#   - Dan Salerno
#   - Brian Silverman

import grid
import functools
import operator

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

_ALL_VALUES = (1, 2, 3, 4, 5, 6, 7, 8, 9)

def possibilities(g):
    """Returns a GridStorage(set) where each element is either all remaining
    possible values for the cell, or None if the cell is already filled out."""
    result_values = []
    for c in g.values:
        if c is None:
            result_values.append(set(_ALL_VALUES))
        else:
            result_values.append(None)
    result = grid.GridStorage(result_values)
    for r in range(9):
        values = set(g.row(r))
        for cell in result.row(r):
            if cell is not None:
                cell.difference_update(values)
    for c in range(9):
        values = set(g.column(c))
        for cell in result.column(c):
            if cell is not None:
                cell.difference_update(values)
    for s in range(9):
        values = set(g.square(s))
        for cell in result.square(s):
            if cell is not None:
                cell.difference_update(values)
    return result

def set_trivial(g):
    """Returns a grid with all the cells that only have one possibility filled
    in. Note that this may leave more cells with one a single possibility in the
    result."""
    p = possibilities(g)
    for r in range(9):
        for c in range(9):
            cell = p.cell(r, c)
            if cell is not None:
                if len(cell) == 1:
                    g = g.set_position(r, c, next(iter(cell)))
    return g

def set_easy(g):
    p = possibilities(g)
    # rows
    for r in range(9):
        for c in range(9):
            valid_count = 0
            valid = ()
            for num in range(1, 10):
                cell = p.cell(r, c)
                if cell is not None and num in cell:
                    if valid_count == 0:
                        valid = (r, c, num)
                        valid_count += 1
                    else:
                        valid_count = 0
                        break

            if valid_count == 1:
                # print("setting " + str(valid))
                g = g.set_position(*valid)
                return g
    # columns
    for c in range(9):
        for r in range(9):
            valid_count = 0
            valid = ()
            for num in range(1, 10):
                cell = p.cell(r, c)
                if cell is not None and num in cell:
                    if valid_count == 0:
                        valid = (r, c, num)
                        valid_count += 1
                    else:
                        valid_count = 0
                        break

            if valid_count == 1:
                # print("setting " + str(valid))
                g = g.set_position(*valid)
                return g

    # boxes
    # for r in range(0, 9, 3):
    #     for c in range(0, 9, 3):
    #         valid_count = 0
    #         valid = ()
    #         for num in range(1, 10):
    #             for i in range(3):
    #                 for j in range(3):
    #                     cell = p.cell(r + i, c + j)
    #                     if cell is not None and num in cell:
    #                         if valid_count == 0:
    #                             valid = (r, c, num)
    #                             valid_count += 1
    #                         else:
    #                             valid_count = 0
    #                             break

    #         if valid_count == 1:
    #             g = g.set_position(*valid)
    #             return g

    return g


def _combined_size(sets):
    """Returns the combined size of an iterable of sets."""
    return functools.reduce(operator.add, (len(s) if s is not None else 0
                                           for s in sets))

def _sorted_by_combined_size(group):
    """Returns indexes into a group of cell possibilities sorted by the smallest
    size, excluding ones which are None."""
    r = []
    for i, l in zip(range(9), iter(group)):
        s = _combined_size(l)
        if s > 0:
            r.append((i, s))
    r.sort(key=operator.itemgetter(1))
    return r

def cells_to_try(p):
    sorted_rows = _sorted_by_combined_size(p.rows())
    sorted_columns = _sorted_by_combined_size(p.columns())
    sorted_squares = _sorted_by_combined_size(p.squares())
    done = set()
    while True:
        row = sorted_rows[0] if sorted_rows else None
        column = sorted_columns[0] if sorted_columns else None
        square = sorted_squares[0] if sorted_squares else None
        if row is None and column is None and square is None:
            return

        if (row is not None
            and (column is None or row[1] <= column[1])
            and (square is None or row[1] <= square[1])):
            sorted_rows.pop(0)
            for c in range(9):
                pos = (row[0], c)
                if pos not in done:
                    done.add(pos)
                    if p.cell(*pos) is not None:
                        yield pos
        elif column is not None and (square is None or column[1] <= square[1]):
            sorted_columns.pop(0)
            for r in range(9):
                pos = (r, column[0])
                if pos not in done:
                    done.add(pos)
                    if p.cell(*pos) is not None:
                        yield pos
        else:
            sorted_squares.pop(0)
            for r in range(square[0] // 3 * 3, square[0] // 3 * 3 + 3):
                for c in range(square[0] % 3 * 3, square[0] % 3 * 3 + 3):
                    pos = (r, c)
                    if pos not in done:
                        done.add(pos)
                        if p.cell(*pos) is not None:
                            yield pos

def solve(g):
    """Returns a solution to g."""
    while True:
        new = set_easy(g)
        if new == g:
            break
        g = new


    while True:
        new = set_trivial(g)
        if new == g:
            break
        g = new


    if not g.is_valid():
        return None
    if g.is_complete():
        return g

    p = possibilities(g)
    for row, column in cells_to_try(p):
        for value in p.cell(row, column):
            result = solve(g.set_position(row, column, value))
            if result is not None:
                return result

    # Failed to solve. Time to try another branch down the possibilities tree.
    return None

def main():
    # Read the file with all the puzzles to solve.
    grid_values = None
    grids = []
    with open("p096_sudoku.txt") as f:
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
                        (int(c) if c != "0" else None for c in line.strip()))
    # Make sure to grab the last grid.
    grids.append(grid.Grid(grid_values))
    assert len(grids) == 50

    euler_answer = 0
    i = 0
    for g in grids:
        # Some basic sanity checking.
        assert not g.is_complete(), "%s is already finished" % (g,)
        assert g.is_valid(), "%s is impossible" % (g,)

        print('Before %d:' % i)
        print(g.pretty())
        solved = solve(g)
        if not solved.is_complete():
            print('------------- Failed to solve %d... ------------' % i)
        else:
            assert solved.is_valid(), (solved,)

            print('After %d:' % i)
            print(solved.pretty())

            euler_answer += solved.euler_answer()
        i += 1
    print('Euler answer: %d' % euler_answer)

if __name__ == "__main__":
    main()
