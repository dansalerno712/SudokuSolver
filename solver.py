#!/usr/bin/python3

# Authors: Jared Bass, Dan Salerno, Brian Silverman
# We pledge our honor that we have abided by the Stevens Honor System
#   - Jared Bass
#   - Dan Salerno
#   - Brian Silverman

import grid
import functools
import operator

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
    if not _possibilities_valid(p):
        return None
    for r in range(9):
        for c in range(9):
            cell = p.cell(r, c)
            if cell is not None and len(cell) == 1:
                g = g.set_position(r, c, next(iter(cell)))
    return g

def _count_possibilities(sets):
    """Returns a list where the value at each index i is the number of cells the
    value i+1 can go in sets."""
    r = [0] * 10
    for cell in sets:
        if cell is not None:
            for value in cell:
                r[value - 1] += 1
    return r

def _find_set_with_value(sets, value):
    """Returns the index into sets which contains value.

    There must be exactly one of these."""
    for i, v in zip(range(9), sets):
        if v is not None and value in v:
            return i
    assert False

def _possibilities_valid(p):
    return all(v is None or v for v in p.values)

def set_easy(g):
    """Returns a grid with one of the values that has only one possible location
    within a row/column/square filled in, or the same grid if there aren't any.

    This only does a single one because all the work needs to be redone to do
    another one anyways, and it generally makes sense to try a set_trivial in
    between successive set_easy calls because that's cheaper."""
    p = possibilities(g)
    if not _possibilities_valid(p):
        return None

    # rows
    for r in range(9):
        row = p.row(r)
        counts = _count_possibilities(row)
        for value in range(1, 10):
            # If there's only one place for the value, then go ahead and set it.
            if counts[value - 1] == 1:
                c = _find_set_with_value(row, value)
                return g.set_position(r, c, value)

    # columns
    for c in range(9):
        column = p.column(c)
        counts = _count_possibilities(column)
        for value in range(1, 10):
            if counts[value - 1] == 1:
                r = _find_set_with_value(column, value)
                return g.set_position(r, c, value)

    # squares
    for s in range(9):
        square = p.square(s)
        counts = _count_possibilities(square)
        for value in range(1, 10):
            if counts[value - 1] == 1:
                i = _find_set_with_value(square, value)
                r = s // 3 * 3 + i // 3
                c = s % 3 * 3 + i % 3
                return g.set_position(r, c, value)

    return g

def _combined_size(sets):
    """Returns the combined size of an iterable of sets."""
    return functools.reduce(operator.add, (len(s) if s is not None else 0
                                           for s in sets))

def _sorted_by_combined_size(group):
    """Returns a list of (i, s) where i is the index into a group of cell
    possibilities and s is its total size, sorted by increasing size."""
    r = []
    for i, l in zip(range(9), iter(group)):
        s = _combined_size(l)
        if s > 0:
            r.append((i, s))
    r.sort(key=operator.itemgetter(1))
    return r

def cells_to_try(p):
    """Generates (row, column) of cells to try filling in. Does this is in an
    optimized order to minimize backtracking fanout."""

    # First, sort all the groups we could use to generate cells.
    sorted_rows = _sorted_by_combined_size(p.rows())
    sorted_columns = _sorted_by_combined_size(p.columns())
    sorted_squares = _sorted_by_combined_size(p.squares())

    # All of the locations we've generated already, to avoid duplicates.
    done = set()

    while True:
        row = sorted_rows[0] if sorted_rows else None
        column = sorted_columns[0] if sorted_columns else None
        square = sorted_squares[0] if sorted_squares else None
        if row is None and column is None and square is None:
            # This means we did all of the groups, so we must be done.
            return

        # If we have a row and neither of the other two has a smaller count.
        if (row is not None
            and (column is None or row[1] <= column[1])
            and (square is None or row[1] <= square[1])):
            # Remove this row because we're going to use it.
            sorted_rows.pop(0)
            # Now go through all the cells in it and yield it iff it doesn't
            # already have a value.
            for c in range(9):
                pos = (row[0], c)
                if pos not in done:
                    done.add(pos)
                    if p.cell(*pos) is not None:
                        yield pos
        # If we have a column and the square doesn't have a smaller count.
        elif column is not None and (square is None or column[1] <= square[1]):
            sorted_columns.pop(0)
            for r in range(9):
                pos = (r, column[0])
                if pos not in done:
                    done.add(pos)
                    if p.cell(*pos) is not None:
                        yield pos
        # Otherwise we must have a square, so use it.
        else:
            sorted_squares.pop(0)
            for r in range(square[0] // 3 * 3, square[0] // 3 * 3 + 3):
                for c in range(square[0] % 3 * 3, square[0] % 3 * 3 + 3):
                    pos = (r, c)
                    if pos not in done:
                        done.add(pos)
                        if p.cell(*pos) is not None:
                            yield pos

def solve(g, seen_grids):
    """Returns a solution to g, or None if it's not possible. seen_grids is a
    set of grids which have already been tried as solutions to this puzzle, and
    so must not be on the untried path to any solutions."""
    if not g.is_valid() or g in seen_grids:
        # If g is already in seen_grids and it was on the path to the solution,
        # we would've found it already and not be here. Therefore, it must not
        # lead to the solution, so just stop now.
        return None
    seen_grids.add(g)

    # Alternate set_easy and set_trivial until they stop finding stuff, or bail
    # out early if they generate something we've already seen or that we can
    # easily tell won't lead to a solution.
    while True:
        new = set_easy(g)
        if new is None or not new.is_valid() or (new != g and new in seen_grids):
            return None
        new = set_trivial(new)
        if new is None or not new.is_valid() or (new != g and new in seen_grids):
            return None
        if new == g:
            break
        seen_grids.add(new)
        g = new

    if g.is_complete():
        # Yay, we're done!
        return g

    p = possibilities(g)
    for row, column in cells_to_try(p):
        for value in p.cell(row, column):
            result = solve(g.set_position(row, column, value), seen_grids)
            if result is not None:
                # If it returned something, we found the solution, so propagate
                # it back up.
                return result

    # Failed to solve. Time to backtrack and try another branch down the
    # possibilities tree.
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

        print("Before %d:" % i)
        print(g.pretty())
        solved = solve(g, set())
        if solved is None or not solved.is_complete():
            raise "------------- Failed to solve %d... ------------" % i
        else:
            assert solved.is_valid(), (solved,)
            assert solved.matches(g), (solved, g)

            print("After %d:" % i)
            print(solved.pretty())

            euler_answer += solved.euler_answer()
        i += 1
    print("Euler answer: %d" % euler_answer)

if __name__ == "__main__":
    main()
