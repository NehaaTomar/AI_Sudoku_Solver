from copy import deepcopy

def is_valid(grid, row, col, num, size):
    """
    Check if placing `num` at (row, col) is valid according to Sudoku rules.
    """
    block_size = int(size ** 0.5)

    # Row and Column Check
    for i in range(size):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    # Subgrid (block) Check
    start_row = (row // block_size) * block_size
    start_col = (col // block_size) * block_size
    for i in range(block_size):
        for j in range(block_size):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty(grid, size):
    """
    Find the next empty cell (marked as 0).
    Returns a tuple (row, col) or None if no empty cells.
    """
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_csp(grid):
    """
    Solve the Sudoku puzzle using constraint satisfaction (backtracking).
    Modifies the grid in-place and returns True if solved, else False.
    """
    size = len(grid)

    def backtrack():
        empty = find_empty(grid, size)
        if not empty:
            return True  # Puzzle is complete

        row, col = empty
        for num in range(1, size + 1):
            if is_valid(grid, row, col, num, size):
                grid[row][col] = num
                if backtrack():
                    return True
                grid[row][col] = 0  # Backtrack

        return False

    return backtrack()
