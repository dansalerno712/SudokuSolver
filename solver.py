#Jared Bass, Dan Salerno, Brian Silverman
#We pledge our honor that we have abided by the Stevens Honor System

import itertools

#Single array to save time creating it over and over. Is reset to full Nones after each check
checking = [None, None, None, None, None, None, None, None, None]

def unique(l):
    """Checks if a list contains all unique items in O(n) time"""
    returning = False
    for item in l:
        if checking[item-1] == None:
            checking[item-1] = 1
        else:
            returning = True
            break

    for i in range(9):
        checking[i] = None

    return returning

def is_valid(grid, row, col):
    """Checks if the number added at spot row x col is a valid move"""
    #Checks if row has unique numbers
    p1 = unique(grid[row])
    #Checks if column has unique numbers: TODO
    p2 = False
    #Checks if box has unique numbers: TODO
    p3 = False

    return p1 and p2 and p3

def chunks(l, n):
    """Yield successive n-sized chunks from list l.
    l: a list
    n: chucnk size"""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def prettyPrint(grid):
    pass

def example_solution():
    return [[4, 8, 3, 9, 2, 1, 6, 5, 7],
            [9, 6, 7, 3, 4, 5, 8, 2, 1],
            [2, 5, 1, 8, 7, 6, 4, 9, 3],
            [5, 4, 8, 1, 3, 2, 9, 7, 6],
            [7, 2, 9, 5, 6, 4, 1, 3, 8],
            [1, 3, 6, 7, 9, 8, 2, 4, 5],
            [3, 7, 2, 6, 8, 9, 5, 1, 4],
            [8, 1, 4, 2, 5, 3, 7, 6, 9],
            [6, 9, 5, 4, 1, 7, 3, 8, 2]]


#This could work but it may run in O(n^2)
def group_ok(group):
    """Returns True/False if the group is valid.
    group: A list of integers representing a row, column, or box"""
    # 2 checks
    # 1) The max of the group is 9
    # 2) Making a set with the group and 0 has 10 unique elements.
    # if this fails there had to have been a duplicate or a 0
    # in the group
    return max(group) + 1 == 10 == len(set([0] + group))


def is_solved(grid):
    """Checks to see if a sudoku grid is solved
    grid: A list of lists of integers representing a sudoku grid"""

    # check rows
    for row in grid:
        if group_ok(row) is False:
            return False

    # transpose the grid to swap rows and columns
    transposed = list(zip(*grid))

    # check columns
    for col in transposed:
        # we need to do list(col) b/c zip returns a bunch of
        # tuples not lists
        if group_ok(list(col)) is False:
            return False

    # check boxes
    for i in range(0, len(grid), 3):
        for j in range(0, len(grid[0]), 3):
            # get the 3x3 box
            box = [row[j:j + 3] for row in grid[i:i + 3]]
            # flatten the 3x3 box into a 1x9 list
            box = list(itertools.chain(*box))
            if group_ok(box) is False:
                return False

    # if everything else passes then its valid so return True
    return True


def pretty_print(grid):
    """Somewhat pretty printing of a sudoku grid"""
    # end="" is to make print not have a newline
    # horizontal line for reuse
    horizontal_line = " -" * 9
    for i in range(len(grid)):
        # print horizontal line at beginning, and every 3 horizontal lines
        if i % 3 == 0:
            print(horizontal_line)
        for j in range(len(grid[0])):
            # print vertical line at beginning, and every 3 vertical lines
            if j == 0:
                print("| ", end="")
            elif j % 3 == 0:
                print(" | ", end="")

            # print the actual number
            print(grid[i][j], end="")
        # ending vertical line
        print(" |")
    # ending horizontal line
    print(horizontal_line)

def main():
    # hardcoding the file_name because im lazy
    file_name = "p096_sudoku.txt"
    grids = []

    # read the file
    with open(file_name) as f:
        # this section does a whole bunch of stuff
        # 1) Ignore the lines that label the puzzles
        # 2) Strip the lines of the actual grid
        # 3) Convert each line of the grid from a string to a list of characters
        # 4) Convert each character in the list to an integer
        # This returns all the lines as a list of lists of integers
        lines = [list(map(int, list(line.strip())))
                 for line in f.readlines() if "Grid" not in line]

    # splits the list of list of grid lines into chunks of 9 lines to break them
    # into puzzles
    grids = list(chunks(lines, 9))
    print(grids[0])
    prettyPrint(grids[0])
    pretty_print(grids[0])

    # testing the is_solved() function
    for grid in grids:
        assert(is_solved(grid) is False)
    assert(is_solved(example_solution()) is True)

if __name__ == '__main__':
    main()
