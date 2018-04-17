def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def prettyPrint(grid):
    """Somewhat pretty printing of a sudoku grid"""
    # end="" is to make print not have a newline
    # horizontal line for reuse
    horizontalLine = " -" * 9
    for i in range(len(grid)):
        # print horizontal line at beginning, and every 3 horizontal lines
        if i % 3 == 0:
            print(horizontalLine)
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
    print(horizontalLine)


def main():
    # hardcoding the filename because im lazy
    fileName = "p096_sudoku.txt"
    grids = []

    # read the file
    with open(fileName) as f:
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
    prettyPrint(grids[0])


if __name__ == '__main__':
    main()
