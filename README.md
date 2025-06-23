# 🧠 AI Sudoku Solver & Generator Web App

This is a full-stack AI-powered Sudoku web application built with **Flask** for the backend and **HTML/CSS/JS** for the frontend.

✅ Supports 4×4, 9×9, 16×16  
🧠 Solves puzzles using CSP and Neural Network  
📊 Leaderboard with avatars  
🎮 Play directly in your browser
## 🎥 Demo Video: AI Sudoku Solver

[![Watch the video](https://img.youtube.com/vi/LtE_hEUltw4/0.jpg)](https://youtu.be/LtE_hEUltw4)

Click the image above or [watch on YouTube](https://youtu.be/LtE_hEUltw4) to see the AI Sudoku Solver in action.

---

## 🚀 Features

| Feature                   | Description |
|---------------------------|-------------|
| 🎮 Sudoku Gameplay        | Play 4x4, 9x9, or 16x16 puzzles |
| 🧩 Puzzle Generator       | Difficulty levels: Easy, Medium, Hard |
| 🤖 AI Solvers             | CSP (all sizes), Neural Net (9x9 only) |
| 📝 Real-Time Validation   | Checks correctness as you play |
| 🏆 Leaderboard            | Stores best scores and avatars |
| 📤 Avatar Upload          | Upload profile pics for leaderboard |
| 🧠 NN Model Training      | Train your own neural model using `train.py` |
| 🗃 SQLite with Alembic    | Database with migrations using Alembic |

---

## 📂 Project Structure

```
project-sudoku/
├── ai-sudoku-solver/
│   ├── app.py                 # Main Flask app
│   ├── create_db.py           # DB setup script
│   ├── generator.py           # Puzzle generator logic
│   ├── predict.py             # Wrapper for NN model prediction
│   ├── solver_csp.py          # CSP-based solver (any size)
│   ├── solver_nn.py           # Neural Network-based solver (9x9 only)
│   ├── train.py               # Model training script
│   ├── sudoku_model.h5        # Pre-trained Keras model
│   ├── requirementr           # Requirements file (should rename to `requirements.txt`)
│   ├── leaderboard.db         # SQLite DB (if used directly)
│   ├── leaderboard.json       # JSON leaderboard (legacy?)
│   ├── static/                # CSS, JS, Avatars
│   ├── templates/             # Jinja templates (index.html etc.)
│   ├── instance/              # Flask instance folder
│   ├── migrations/            # Alembic DB migrations
│   └── app.db                 # Final SQLite database
├── .vscode/                   # (Optional) VS Code settings
├── alembic.ini                # Alembic config
├── Al Sudoku Solver.mp4       # (Optional) Demo video
```

---

## 🛠️ Installation

### 1. Clone the Repo

```bash
git clone https://github.com/NehaaTomar/AI_Sudoku_Solver.git
cd ai-sudoku-solver
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

First, rename the `requirementr` file to `requirements.txt`:

```bash
mv requirementr requirements.txt
pip install -r requirements.txt
```

Or manually install essentials:

```bash
pip install flask flask_sqlalchemy numpy keras tensorflow alembic
```

### 4. Initialize Database

```bash
python create_db.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### 5. Run the App

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧠 API Endpoints

### `GET /generate`
Returns a new Sudoku puzzle.

**Query Parameters:**
- `size`: 4, 9, or 16
- `difficulty`: easy, medium, or hard

---

### `POST /solve`
Solves a given puzzle.

```json
{
  "grid": [[...]],
  "method": "csp" | "nn"
}
```

Returns:
```json
{ "solution": [[...]] }
```

---

### `POST /validate`
Checks if current grid is valid.

```json
{ "grid": [[...]] }
```

Returns:
```json
{ "valid": true }
```

---

### `POST /submit_score`
Submit score and optional avatar.

- Fields: `name`, `time`, `difficulty`, `grid_size`, `avatar` (file)

---

### `GET /leaderboard`
Returns leaderboard JSON:

```json
[
  {
    "name": "Bob",
    "time": 120.5,
    "difficulty": "medium",
    "grid_size": "9",
    "avatar": "/static/avatars/..."
  },
  ...
]
```

---

## 🧠 AI Solvers

### CSP Solver (`solver_csp.py`)
- Works with all grid sizes.
- Uses backtracking with constraint propagation.

### Neural Net Solver (`solver_nn.py`)
- Works **only for 9×9 puzzles**
- Requires `sudoku_model.h5`
- Train your model with `train.py`

---

## 🧪 Training Neural Model

To retrain the model:

```bash
python backend/train.py
```

This saves a new `sudoku_model.h5` file which is loaded by `predict.py`.

---

## 🧑‍💻 Contributing

1. Fork the repo  
2. Create a branch: `git checkout -b feature-xyz`  
3. Commit and push  
4. Create a PR  

PRs are welcome!

---

## 🖼️ Screenshots
![Game](/images/Game.png)
![Avatar](/images/Avatar.png)
![sudokusolver](/images/sudokusolver.png)
![AI](/images/AI.png)
![theme](/images/theme.png)
![leaderboard](/images/leaderboard.png)


---

## 📜 License

This project is licensed under the MIT License.
[MIT LICENSE](LICENSE.txt)
---

## 🙋 FAQ

**Q: Why doesn’t the neural net work on 4x4 or 16x16?**  
A: It's trained only for standard 9x9 Sudoku.

**Q: How are avatars handled?**  
A: They're stored in `/static/avatars` and linked to player scores.

**Q: What is `leaderboard.json` for?**  
A: Legacy format—use SQLite database (`app.db` or `leaderboard.db`) for persistence.


## 📬 Connect with Me

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-blue?style=for-the-badge)](https://inspiring-palmier-dd7dd4.netlify.app/)
[![GitHub](https://img.shields.io/badge/GitHub-NehaaTomar-black?style=for-the-badge&logo=github)](https://github.com/NehaaTomar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/neha-tomar-52b212224)
[![Gmail](https://img.shields.io/badge/Gmail-MailMe-red?style=for-the-badge&logo=gmail)](mailto:nehatomar349@gmail.com)


---

---

