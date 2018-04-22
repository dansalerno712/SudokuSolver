# Authors: Jared Bass, Dan Salerno, Brian Silverman
# We pledge our honor that we have abided by the Stevens Honor System
#   - Jared Bass
#   - Dan Salerno
#   - Brian Silverman

import util

def _filter_nones(l):
    """Generates all the elements in l which are not None."""
    return (i for i in l if i is not None)

def _is_unique(l):
    """Checks if a list contains all unique items (except possible Nones)
    quickly.

    Note that although this is technically O(N log N), and other possible
    algorithms are O(N), in practice N=9 so the constant overhead matters
    way more and this is faster."""
    no_nones = list(_filter_nones(l))
    return len(no_nones) == len(set(no_nones))

def _min_and_max(l):
    """Returns (min, max) of l ignoring Nones.

    Returns (None, None) if there are no non-None elements in l."""
    min_r, max_r = None, None
    for e in _filter_nones(l):
        if min_r is None or e < min_r:
            min_r = e
        if max_r is None or e > max_r:
            max_r = e
    return min_r, max_r

class Grid(object):
    """An immutable object representing a complete grid of numbers, or None to
    indicate blank squares.

    We store the values in a single tuple, and expose them in various
    convenient ways via accessors. Doing it this way makes creating modified
    copies cheap (create list and assign), and the only downside is one of the
    many ways of accessing the data could potentially be simpler.

    All locations are identified via 0-based row-major indexing, and values are
    the actual 1-based values.

    All locations indices start in the upper left corner. That is, these are the
    3x3 squares, and also the cells within each square:
        |---+---+---|
        | 0 | 1 | 2 |
        |---+---+---|
        | 3 | 4 | 5 |
        |---+---+---|
        | 6 | 7 | 8 |
        |---+---+---|
    And these are the rows:
        |-----------|
        | 000000000 |
        | 111111111 |
        | 222222222 |
        | 333333333 |
        | 444444444 |
        | 555555555 |
        | 666666666 |
        | 777777777 |
        | 888888888 |
        |-----------|
    And these are the columns:
        |-----------|
        | 012345678 |
        | 012345678 |
        | 012345678 |
        | 012345678 |
        | 012345678 |
        | 012345678 |
        | 012345678 |
        | 012345678 |
        | 012345678 |
        |-----------|
    """

    def __init__(self, values):
        self._values = tuple(values)
        assert len(self._values) == 9 * 9, "invalid length"

        min_in, max_in = _min_and_max(self._values)
        assert min_in is None or min_in >= 1, "invalid value"
        assert max_in is None or max_in <= 9, "invalid value"

    def __repr__(self):
        return "Grid(%s)" % repr(self._values)

    def __eq__(self, other):
        return self._values == other._values

    def __hash__(self):
        # Don't hash to the same as just the values tuple, because that could be
        # undesirable for some use cases.
        return hash(tuple(self._values, 971))

    def cell(self, row, column):
        """Returns the value at the specified row and column."""
        return self._values[row * 9 + column]

    def square(self, index):
        """Returns a tuple with the values for the specified square."""
        start_position = (index // 3) * (9 * 3) + (index % 3) * 3
        top = self._values[start_position:start_position + 3]
        start_position += 9
        middle = self._values[start_position:start_position + 3]
        start_position += 9
        bottom = self._values[start_position:start_position + 3]
        return top + middle + bottom

    def row(self, index):
        """Returns a tuple with the values for the specified row."""
        start_position = index * 9
        return self._values[start_position:start_position + 9]

    def column(self, index):
        """Returns a tuple with the values for the specified column."""
        return self._values[index::9]

    def is_complete(self):
        """Returns True if there are no None (unknown) values.

        Note that this does not mean it is a valid solution."""
        return not not next(filter(lambda x: x is None, self._values), True)

    def is_valid(self):
        """Returns True if there are no conflicting values.

        Note that this deliberately ignores multiple None values."""
        for r in range(9):
            if not _is_unique(self.row(r)):
                return False
        for c in range(9):
            if not _is_unique(self.column(c)):
                return False
        for s in range(9):
            if not _is_unique(self.square(s)):
                return False
        return True

    def pretty(self):
        """Returns a human-readable representation."""
        horizontal_line = ('+',) + (('-',) * 7 + ('+',)) * 3 + ('\n',)
        r = []
        r.extend(horizontal_line)
        for square_row in range(3):
            for row_index in range(square_row * 3, square_row * 3 + 3):
                for group in util.grouper(self.row(row_index), 3):
                    r.append('| ')
                    for cell in group:
                        r.append(str(cell) if cell is not None else 'x')
                        r.append(' ')
                r.append('|\n')
            r.extend(horizontal_line)
        return ''.join(r[:-1])
