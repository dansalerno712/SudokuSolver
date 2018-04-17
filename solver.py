#Jared Bass, Dan Salerno, Brian Silverman
#We pledge our honor that we have abided by the Stevens Honor System

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
    print(grids[0])
    prettyPrint(grids[0])

if __name__ == '__main__':
    main()
