# 1. Install dependencies
!pip install tensorflow numpy

# 2. Imports
import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, BatchNormalization, ReLU, Flatten, Dense, Reshape, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# 3. CSP Sudoku Solver
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_csp(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_csp(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# 4. Generate Sudoku pairs
def generate_sudoku_pair():
    board = [[0] * 9 for _ in range(9)]
    solve_csp(board)
    full = [row[:] for row in board]

    puzzle = [row[:] for row in full]
    removed = 45
    while removed > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if puzzle[i][j] != 0:
            puzzle[i][j] = 0
            removed -= 1
    return np.array(puzzle), np.array(full)

def generate_dataset(n=1000):
    puzzles, solutions = [], []
    for _ in range(n):
        puzzle, solution = generate_sudoku_pair()
        puzzles.append(puzzle)
        solutions.append(solution)
    return np.array(puzzles), np.array(solutions)

# 5. Prepare Dataset
print("Generating dataset...")
X, y = generate_dataset(1000)
X = X.reshape(-1, 9, 9, 1) / 9.0  # Normalize input
y = y - 1  # Shift labels from 1–9 to 0–8
y = to_categorical(y, num_classes=9)

# 6. Define CNN Model
model = Sequential([
    Conv2D(64, (3, 3), padding='same', input_shape=(9, 9, 1)),
    BatchNormalization(), ReLU(),
    Conv2D(64, (3, 3), padding='same'),
    BatchNormalization(), ReLU(),
    Dropout(0.3),
    Conv2D(81, (1, 1), activation='relu'),  # Per-cell prediction
    Flatten(),
    Dense(729, activation='softmax'),  # Softmax per digit
    Reshape((81, 9))
])

model.compile(loss='categorical_crossentropy', optimizer=Adam(1e-3), metrics=['accuracy'])

# 7. Train
print("Training model...")
model.fit(
    X, y.reshape(-1, 81, 9),
    epochs=5,
    batch_size=64,
    validation_split=0.1
)

# 8. Save model
model.save("sudoku_model.h5")
print("✅ Model saved as sudoku_model.h5")

# 9. Download model
from google.colab import files
files.download("sudoku_model.h5")
