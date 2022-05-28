## Sudoku solver
Solves given sudoku using PySAT library.

### How to use
1. Have valid empty sudoku in .txt file. Valid empty sudoku has size of NxN, has only integers and all integers are from range {0, 1, ..., N-1, N} where 0 means that cell is empty.
2. Run in commad line, like `python3 sudoku.py problem.txt` or `python3 sudoku.py problem.txt > solved.txt` if you want solution into .txt file instead of just printing it.