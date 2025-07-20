import os
import numpy as np
import torch
import torch.nn as nn
from tensorflow.keras.models import load_model
from typing import List, Literal

# -----------------------------
# Constants and Model Loading
# -----------------------------

KERAS_MODEL_PATH = "backend/sudoku_model.h5"
PYTORCH_MODEL_PATH = "backend/sudoku_model.pth"

try:
    keras_model = load_model(KERAS_MODEL_PATH)
    print(f"[INFO] Keras model loaded from '{KERAS_MODEL_PATH}'")
except Exception as e:
    print(f"[ERROR] Failed to load Keras model: {e}")
    keras_model = None


# -----------------------------
# Keras CNN Sudoku Solver
# -----------------------------

def solve_with_keras(grid: List[List[int]]) -> List[List[int]]:
    """
    Solve a 9x9 Sudoku puzzle using a Keras CNN model.
    """
    if keras_model is None:
        raise RuntimeError("Keras model is not loaded.")

    if not is_valid_grid(grid):
        raise ValueError("Input grid must be 9x9 with integers.")

    board = np.array(grid).reshape(1, 9, 9, 1).astype(np.float32) / 9.0
    prediction = keras_model.predict(board, verbose=0)
    prediction = prediction.argmax(axis=-1).reshape(9, 9) + 1
    return prediction.tolist()


# -----------------------------
# PyTorch MLP Sudoku Solver
# -----------------------------

class SudokuNet(nn.Module):
    def __init__(self):
        super(SudokuNet, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(81, 512),
            nn.ReLU(),
            nn.Linear(512, 81)
        )

    def forward(self, x):
        return self.model(x)


def solve_with_pytorch(grid: List[List[int]], model_path: str = PYTORCH_MODEL_PATH) -> List[List[int]]:
    """
    Solve a 9x9 Sudoku puzzle using a PyTorch MLP model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"PyTorch model not found at '{model_path}'")

    if not is_valid_grid(grid):
        raise ValueError("Input grid must be 9x9 with integers.")

    model = SudokuNet()
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()

    board_flat = np.array(grid).reshape(1, 81).astype(np.float32) / 9.0
    input_tensor = torch.tensor(board_flat, dtype=torch.float32)

    with torch.no_grad():
        output = model(input_tensor).view(9, 9)
        solved = output.round().clamp(1, 9).int()

    return solved.tolist()


# -----------------------------
# Unified Solver Interface
# -----------------------------

def solve_nn(grid: List[List[int]], method: Literal["keras", "pytorch"] = "keras") -> List[List[int]]:
    """
    Solve Sudoku using a selected neural network method.

    Args:
        grid (List[List[int]]): 9x9 Sudoku grid with 0s for empty cells.
        method (str): Either 'keras' or 'pytorch'.

    Returns:
        List[List[int]]: Solved 9x9 Sudoku grid.
    """
    if not is_valid_grid(grid):
        raise ValueError("Grid must be a 9x9 list of lists containing integers 0–9.")

    if method == "keras":
        return solve_with_keras(grid)
    elif method == "pytorch":
        return solve_with_pytorch(grid)
    else:
        raise ValueError("Invalid method. Choose 'keras' or 'pytorch'.")


# -----------------------------
# Utility: Grid Validation
# -----------------------------

def is_valid_grid(grid: List[List[int]]) -> bool:
    """
    Validates that the input is a 9x9 list of lists with integers 0–9.
    """
    if not isinstance(grid, list) or len(grid) != 9:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False
        if not all(isinstance(cell, int) and 0 <= cell <= 9 for cell in row):
            return False
    return True
