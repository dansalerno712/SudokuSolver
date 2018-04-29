# SudokuSolver
Sudoku Solver for the final project of CS370

# Authors: Jared Bass, Dan Salerno, Brian Silverman
 We pledge our honor that we have abided by the Stevens Honor System
   - Jared Bass
   - Dan Salerno
   - Brian Silverman

 Note that the `p096_sudoku.txt` file is downloaded from Project Euler.

# Tests
We have unit tests for some of the easier-to-test parts of our code where tests
have the most value.
```console
$ ./test.sh 
+ ./grid_test.py
.........
----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK
+ ./solver_test.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.018s

OK
```

The main program itself self-validates. Verifying that a solution to an
individual puzzle is pretty simple. It must:
  * Have all the cells filled in
  * Be a valid grid (each row/column/square has all 9 numbers exactly once)
  * Match the given hints
We have code which validates this and assert-fails if any of them are not true.
It also prints out the final answer, which matches the golden value of `24702`.
