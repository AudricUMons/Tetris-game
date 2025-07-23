const TILE_SIZE = 30;
const COLS = 10;
const ROWS = 20;
const MARGIN = 10;
const WIDTH = COLS * TILE_SIZE;
const HEIGHT = ROWS * TILE_SIZE;
const FPS = 60;

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const nextCanvas = document.getElementById("next");
const nextCtx = nextCanvas.getContext("2d");
const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");
const linesEl = document.getElementById("lines");

const sounds = {
  rotate: new Audio("../assets/m.wav"),
  place: new Audio("../assets/m.wav"),
  clear: new Audio("../assets/m.wav"),
  gameover: new Audio("../assets/m.wav")
};

const TETROMINOS = [
  { shape: [[-1,0],[0,0],[1,0],[2,0]], color: "#0ff" },
  { shape: [[0,0],[1,0],[0,1],[1,1]], color: "#ff0" },
  { shape: [[-1,0],[0,0],[1,0],[0,1]], color: "#a0f" },
  { shape: [[-1,0],[0,0],[1,0],[1,1]], color: "#fa0" },
  { shape: [[-1,0],[0,0],[1,0],[-1,1]], color: "#00f" },
  { shape: [[0,0],[1,0],[-1,1],[0,1]], color: "#0f0" },
  { shape: [[-1,0],[0,0],[0,1],[1,1]], color: "#f00" }
];

class Piece {
  constructor(id) {
    this.id = id;
    this.shape = TETROMINOS[id].shape.map(([x,y]) => [x,y]);
    this.color = TETROMINOS[id].color;
    this.pos = [Math.floor(COLS / 2), 0];
  }

  rotate() {
    this.shape = this.shape.map(([x, y]) => [-y, x]);
  }

  getCells() {
    return this.shape.map(([x, y]) => [this.pos[0] + x, this.pos[1] + y]);
  }
}

class Tetris {
  constructor() {
    this.reset();
  }

  reset() {
    this.board = Array.from({length: ROWS}, () => Array(COLS).fill(-1));
    this.score = 0;
    this.level = 1;
    this.lines = 0;
    this.flashingRows = [];
    this.flashStartTime = null;
    this.flashDelay = 300;
    this.gameOver = false;
    document.getElementById("gameover").style.display = "none"; 
    this.next = this.randomPiece();
    this.spawn();
  }

  randomPiece() {
    return new Piece(Math.floor(Math.random() * TETROMINOS.length));
  }

    spawn() {
    this.piece = this.next;
    this.next = this.randomPiece();
    if (!this.valid(this.piece.getCells())) {
        this.gameOver = true;
        sounds.gameover.play();
        document.getElementById("gameover").style.display = "block";  // ⬅️ Cette ligne est ESSENTIELLE
    }
    }

  clearFlashingLines() {
  this.board = this.board.filter((row, y) => !this.flashingRows.includes(y));
  while (this.board.length < ROWS) this.board.unshift(Array(COLS).fill(-1));
  this.score += this.flashingRows.length * 100;
  this.lines += this.flashingRows.length;
  this.level = 1 + Math.floor(this.lines / 10);
  sounds.clear.play();
}


  valid(cells) {
    return cells.every(([x, y]) => x >= 0 && x < COLS && y < ROWS && (y < 0 || this.board[y][x] === -1));
  }

  freeze() {
    for (const [x, y] of this.piece.getCells()) {
      if (y >= 0) this.board[y][x] = this.piece.id;
    }
    sounds.place.play();
  }

  clearLines() {
    let cleared = 0;
    this.board = this.board.filter(row => {
      if (row.every(cell => cell !== -1)) {
        cleared++;
        return false;
      }
      return true;
    });
    while (this.board.length < ROWS) this.board.unshift(Array(COLS).fill(-1));
    if (cleared > 0) {
      this.score += cleared * 100;
      this.lines += cleared;
      this.level = 1 + Math.floor(this.lines / 10);
      sounds.clear.play();
    }
  }

  prepareLineClear() {
    this.flashingRows = [];
    for (let y = 0; y < ROWS; y++) {
        if (this.board[y].every(cell => cell !== -1)) {
        this.flashingRows.push(y);
        }
    }
    if (this.flashingRows.length > 0) {
        this.flashStartTime = performance.now();
    } else {
        this.spawn(); // aucune ligne à effacer
    }
    }


  move(dx, dy, rotate = false) {
    if (this.gameOver) return;
    const newPiece = new Piece(this.piece.id);
    newPiece.shape = rotate ? this.piece.shape.map(([x,y]) => [-y, x]) : this.piece.shape.map(([x,y]) => [x,y]);
    newPiece.pos = [this.piece.pos[0] + dx, this.piece.pos[1] + dy];
    if (this.valid(newPiece.getCells())) {
      this.piece = newPiece;
      if (rotate) sounds.rotate.play();
    } else if (dy === 1) {
      this.freeze();
      this.prepareLineClear();
    }
  }

  ghost() {
    let ghostY = this.piece.pos[1];
    while (true) {
      ghostY++;
      const cells = this.piece.shape.map(([x,y]) => [this.piece.pos[0]+x, ghostY+y]);
      if (!this.valid(cells)) break;
    }
    return this.piece.shape.map(([x,y]) => [this.piece.pos[0]+x, ghostY-1+y]);
  }

  hexToRgba(hex, alpha) {
  const bigint = parseInt(hex.slice(1), 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha.toFixed(2)})`;
}


  draw(ctx) {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    drawGrid(ctx);
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            const id = this.board[y][x];
            if (id !== -1) {
            const isFlashing = this.flashingRows && this.flashingRows.includes(y);
            if (isFlashing) {
                const alpha = Math.abs(Math.sin(performance.now() / 100));
                ctx.fillStyle = this.hexToRgba(TETROMINOS[id].color, alpha);
                ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1);
            } else {
                this.drawTile(ctx, x, y, TETROMINOS[id].color);
            }
            }
        }
    }

    for (const [x,y] of this.ghost()) {
        ctx.fillStyle = "rgba(255,255,255,0.2)";
        ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1);
    }
    for (const [x,y] of this.piece.getCells()) {
        if (y >= 0) this.drawTile(ctx, x, y, this.piece.color);
    }
    };

  drawTile(ctx, x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1);
  }

  drawNext(ctx) {
    ctx.clearRect(0, 0, 120, 120);
    for (const [x,y] of this.next.shape) {
      ctx.fillStyle = this.next.color;
      ctx.fillRect((x+2) * 30, (y+2) * 30, 29, 29);
    }
  }
}

const game = new Tetris();
let dropCounter = 0;
let dropInterval = 500;
let lastTime = 0;

function update(time = 0) {
  const delta = time - lastTime;
  lastTime = time;
  dropCounter += delta;

    if (game.flashingRows.length > 0 && game.flashStartTime !== null) {
        if (time - game.flashStartTime > game.flashDelay) {
            game.clearFlashingLines();
            game.spawn();
            game.flashingRows = [];
            game.flashStartTime = null;         
        }
    }


  if (dropCounter > dropInterval - game.level * 25) {
    game.move(0, 1);
    dropCounter = 0;
  }
  game.draw(ctx);
  game.drawNext(nextCtx);
  scoreEl.textContent = game.score;
  levelEl.textContent = game.level;
  linesEl.textContent = game.lines;
  requestAnimationFrame(update);
}

function drawGrid(ctx) {
    ctx.strokeStyle = "#333";
    for (let x = 0; x <= COLS; x++) {
        ctx.beginPath();
        ctx.moveTo(x * TILE_SIZE, 0);
        ctx.lineTo(x * TILE_SIZE, HEIGHT);
        ctx.stroke();
    }
    for (let y = 0; y <= ROWS; y++) {
        ctx.beginPath();
        ctx.moveTo(0, y * TILE_SIZE);
        ctx.lineTo(WIDTH, y * TILE_SIZE);
        ctx.stroke();
    }
}

document.addEventListener("keydown", e => {
  // Restart avec R si game over
  if (game.gameOver && e.key.toLowerCase() === 'r') {
    game.reset();
    return;
  }

  // Bloquer toutes les autres touches si game over
  if (game.gameOver) return;

  if (e.key === "ArrowLeft") game.move(-1, 0);
  else if (e.key === "ArrowRight") game.move(1, 0);
  else if (e.key === "ArrowDown") game.move(0, 1);
  else if (e.key === "ArrowUp") game.move(0, 0, true);
  else if (e.code === "Space") {
    while (true) {
      const nextY = game.piece.pos[1] + 1;
      const testCells = game.piece.shape.map(([x, y]) => [game.piece.pos[0] + x, nextY + y]);
      if (game.valid(testCells)) {
        game.piece.pos[1]++;
      } else {
        break;
      }
    }
    game.freeze();
    game.prepareLineClear();  // si tu utilises l'animation maintenant
  }
});


update();
