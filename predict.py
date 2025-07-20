# predict.py
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("backend/sudoku_model.h5")

def predict_sudoku(puzzle):
    """
    puzzle: 9x9 numpy array with values 0-9 (0 = empty)
    returns: 9x9 numpy array with predicted values
    """
    input_data = puzzle.reshape(1, 9, 9, 1) / 9.0  # Normalize
    predictions = model.predict(input_data)
    predictions = predictions.reshape(81, 9)

    # Choose the digit with the highest probability
    digits = np.argmax(predictions, axis=1) + 1
    solved = digits.reshape(9, 9)

    # Keep original clues; only fill blanks
    output = puzzle.copy()
    for i in range(9):
        for j in range(9):
            if output[i][j] == 0:
                output[i][j] = solved[i][j]
    return output

# Example usage
if __name__ == "__main__":
    example_puzzle = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

    print("Input Puzzle:")
    print(example_puzzle)

    solution = predict_sudoku(example_puzzle)

    print("\nPredicted Solution:")
    print(solution)
