let timerInterval;
let startTime;

function startTimer() {
  clearInterval(timerInterval);
  startTime = new Date();
  timerInterval = setInterval(() => {
    const now = new Date();
    const seconds = Math.floor((now - startTime) / 1000);
    const min = String(Math.floor(seconds / 60)).padStart(2, '0');
    const sec = String(seconds % 60).padStart(2, '0');
    document.getElementById("timer").textContent = `⏱ ${min}:${sec}`;
  }, 1000);
}

function generate(difficulty) {
  fetch(`/generate?difficulty=${difficulty}`)
    .then(res => res.json())
    .then(data => {
      loadBoard(data.puzzle);
      startTimer();
    });
}

function loadBoard(board) {
  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      const cell = document.getElementById(`cell${i}${j}`);
      cell.value = board[i][j] !== 0 ? board[i][j] : "";
    }
  }
}

function resetBoard() {
  const cells = document.querySelectorAll("input");
  cells.forEach(cell => cell.value = "");
  clearInterval(timerInterval);
  document.getElementById("timer").textContent = "⏱ 00:00";
}

function getHint() {
  const grid = getBoard();
  fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grid: grid, method: "csp", hint: true })
  })
  .then(res => res.json())
  .then(data => {
    if (data.puzzle) loadBoard(data.puzzle);
  });
}

function getBoard() {
  const grid = [];
  for (let i = 0; i < 9; i++) {
    const row = [];
    for (let j = 0; j < 9; j++) {
      const val = document.getElementById(`cell${i}${j}`).value;
      row.push(val === "" ? 0 : parseInt(val));
    }
    grid.push(row);
  }
  return grid;
}

document.getElementById("sudoku-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const grid = getBoard();
  fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grid: grid, method: "csp" })
  })
    .then(res => res.json())
    .then(data => {
      loadBoard(data.solution);
      clearInterval(timerInterval);
    });
});
