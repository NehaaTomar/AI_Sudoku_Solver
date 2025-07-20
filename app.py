from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import os
from werkzeug.utils import secure_filename

from solver_csp import solve_csp
from solver_nn import solve_nn
from generator import generate_puzzle

# -------------------- App Setup --------------------
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database setup
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Avatar upload setup
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'avatars')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# -------------------- Database Model --------------------
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    grid_size = db.Column(db.String(5), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(100), nullable=True)

# -------------------- Routes --------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['GET'])
def generate_puzzle_route():
    difficulty = request.args.get("difficulty", "medium")
    size = int(request.args.get("size", 9))
    puzzle, solution = generate_puzzle(difficulty, size)
    return jsonify({"puzzle": puzzle, "solution": solution})

@app.route('/solve', methods=['POST'])
def solve():
    try:
        print("Headers:", request.headers)
        print("Raw data:", request.data)

        data = request.get_json(force=False, silent=False)  # Fail fast
        print("Parsed JSON:", data)

        grid = data.get("grid")
        method = data.get("method", "csp")

        size = len(grid)
        if any(len(row) != size for row in grid):
            return jsonify({"error": "Grid is not square"}), 400

        if method == "nn":
            if size != 9:
                return jsonify({"error": "Neural solver only supports 9x9 grids."}), 400
            solution = solve_nn(grid)
        else:
            success = solve_csp(grid)
            if not success:
                return jsonify({"error": "CSP solver failed"}), 400
            solution = grid

        return jsonify({"solution": solution})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/validate", methods=['POST'])
def validate():
    data = request.get_json()
    user_grid = data.get("grid")
    if not user_grid or not isinstance(user_grid, list):
        return jsonify({'valid': False, 'error': 'Invalid grid.'}), 400
    is_valid = validate_sudoku(user_grid)
    return jsonify({'valid': is_valid})

def validate_sudoku(grid):
    size = len(grid)
    block_size = int(np.sqrt(size))
    if block_size * block_size != size:
        return False

    for row in grid:
        nums = [n for n in row if n != 0]
        if len(nums) != len(set(nums)):
            return False

    for col in range(size):
        nums = [grid[row][col] for row in range(size) if grid[row][col] != 0]
        if len(nums) != len(set(nums)):
            return False

    for block_row in range(0, size, block_size):
        for block_col in range(0, size, block_size):
            block_nums = []
            for i in range(block_size):
                for j in range(block_size):
                    val = grid[block_row + i][block_col + j]
                    if val != 0:
                        block_nums.append(val)
            if len(block_nums) != len(set(block_nums)):
                return False

    return True
def solve_csp(grid):
    size = len(grid)
    block_size = int(size ** 0.5)

    def is_valid(r, c, val):
        for i in range(size):
            if grid[r][i] == val or grid[i][c] == val:
                return False
        start_row, start_col = r - r % block_size, c - c % block_size
        for i in range(start_row, start_row + block_size):
            for j in range(start_col, start_col + block_size):
                if grid[i][j] == val:
                    return False
        return True

    def backtrack():
        for r in range(size):
            for c in range(size):
                if grid[r][c] == 0:
                    for val in range(1, size + 1):
                        if is_valid(r, c, val):
                            grid[r][c] = val
                            if backtrack():
                                return True
                            grid[r][c] = 0
                    return False
        return True

    return backtrack()

@app.route("/submit_score", methods=["POST"])
def submit_score():
    try:
        if request.content_type.startswith('multipart/form-data'):
            name = request.form.get("name", "Anonymous")
            time_val = float(request.form.get("time", "0"))
            difficulty = request.form.get("difficulty", "medium")
            grid_size = request.form.get("grid_size", "9")
            avatar_file = request.files.get("avatar")
        else:
            data = request.get_json()
            name = data.get("name", "Anonymous")
            time_val = float(data.get("time", 0))
            difficulty = data.get("difficulty", "medium")
            grid_size = data.get("grid_size", "9")
            avatar_file = None

        avatar_filename = None
        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            avatar_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
            avatar_file.save(avatar_path)

        new_score = Score(
            name=name,
            time=time_val,
            difficulty=difficulty,
            grid_size=grid_size,
            timestamp=datetime.now().isoformat(),
            avatar=avatar_filename
        )
        db.session.add(new_score)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    scores = Score.query.order_by(Score.time.asc()).limit(50).all()
    leaderboard = []
    for s in scores:
        leaderboard.append({
            "name": s.name,
            "time": s.time,
            "difficulty": s.difficulty,
            "grid_size": s.grid_size,
            "timestamp": s.timestamp,
            "avatar": f"/static/avatars/{s.avatar}" if s.avatar else None
        })
    return jsonify(leaderboard)

# -------------------- Main Entry --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
