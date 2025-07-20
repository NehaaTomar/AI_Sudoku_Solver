import random
import copy
from solver_csp import solve_csp

# Difficulty levels: proportion of cells to remove
DIFFICULTY_LEVELS = {
    'easy': 0.4,
    'medium': 0.5,
    'hard': 0.6,
    'extreme': 0.7
}

def is_perfect_square(n: int) -> bool:
    return int(n ** 0.5) ** 2 == n

def generate_full_grid(size=9):
    """
    Generate a fully solved grid of a given size using CSP solver.
    Size must be a perfect square (4, 9, 16, etc.).
    """
    if not is_perfect_square(size):
        raise ValueError("Grid size must be a perfect square (4, 9, 16, etc.)")

    board = [[0 for _ in range(size)] for _ in range(size)]
    solved = solve_csp(board)
    if not solved:
        raise RuntimeError("Failed to generate a solved grid.")
    return board

def remove_cells(board, difficulty='medium'):
    """
    Remove cells from the board to create a puzzle, based on difficulty level.
    Ensures the resulting puzzle still has a solution (not necessarily unique).
    """
    size = len(board)
    puzzle = copy.deepcopy(board)
    perc = DIFFICULTY_LEVELS.get(difficulty, 0.5)
    total_cells = size * size
    target_removals = int(total_cells * perc)
    removed = 0
    attempts = 0
    max_attempts = total_cells * 5

    while removed < target_removals and attempts < max_attempts:
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)

        if puzzle[i][j] != 0:
            backup = puzzle[i][j]
            puzzle[i][j] = 0

            # Optional: Check if still solvable
            puzzle_copy = copy.deepcopy(puzzle)
            if solve_csp(puzzle_copy):
                removed += 1
            else:
                puzzle[i][j] = backup  # Restore if it becomes unsolvable

        attempts += 1

    return puzzle

def generate_puzzle(difficulty='medium', size=9):
    """
    Generate a Sudoku puzzle and its full solution.

    Returns:
        puzzle: grid with removed cells
        solution: fully filled grid
    """
    if not is_perfect_square(size):
        raise ValueError("Grid size must be a perfect square (4, 9, 16, etc.)")

    full_grid = generate_full_grid(size)
    puzzle = remove_cells(full_grid, difficulty)
    return puzzle, full_grid
