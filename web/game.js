// Constants
const GRID_SIZE = 10;
const BLOCK_SIZE = 60; // Size of each block in the grid
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const BLACK = "#000000";
const GREEN = "#00FF00";
const RED = "#FF0000";
const BLUE = "#0000FF";
const PURPLE = "#800080";
const WHITE = "#FFFFFF";
const DARK_GRAY = "#505050";

// Initialize game variables
let playerPos = [0, 0];
let lives = 3;
let gameOver = false;
let grid;
let revealedBlocks = new Set();
let message = "";
let startTime = Date.now();
let gameMode = 'normal'; // Set default game mode to normal

// Show the main menu
function showMainMenu() {
    document.getElementById("mainMenu").style.display = "flex";
    document.getElementById("gameArea").style.display = "none";
}

// Start the game based on the selected mode (Normal or Speedrun)
function startGame(mode) {
    gameMode = mode;
    document.getElementById("mainMenu").style.display = "none";
    document.getElementById("gameArea").style.display = "flex";
    initGame();
}

// Initialize the game
function initGame() {
    grid = generateGrid();
    playerPos = [0, 0];
    revealedBlocks = new Set();
    gameOver = false;
    message = "";
    startTime = Date.now();
    if (gameMode === 'normal') {
        lives = 3; // Normal mode has 3 lives
    }
    updateUI();
    draw();
}

// Generate a grid with paths, dangers, and teleporters
function generateGrid() {
    let grid = Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
    let path = generatePath();

    // Add dangers
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            if (Math.random() < 0.2 && !path.includes(`${x},${y}`) && (x !== 0 || y !== 0)) {
                grid[y][x] = 1; // Dangerous block
            }
        }
    }

    // Add teleporters
    for (let i = 0; i < 3; i++) {
        let x, y;
        do {
            x = Math.floor(Math.random() * GRID_SIZE);
            y = Math.floor(Math.random() * GRID_SIZE);
        } while (grid[y][x] !== 0 || (x === GRID_SIZE - 1 && y === GRID_SIZE - 1));
        grid[y][x] = 3; // Teleporter
    }

    // Goal block
    grid[GRID_SIZE - 1][GRID_SIZE - 1] = 2; // True goal
    return grid;
}

// Generate the correct path from start to finish
function generatePath() {
    let path = [];
    let x = 0, y = 0;
    path.push(`${x},${y}`);

    while (x !== GRID_SIZE - 1 || y !== GRID_SIZE - 1) {
        if (x < GRID_SIZE - 1 && (Math.random() < 0.5 || y === GRID_SIZE - 1)) {
            x++;
        } else {
            y++;
        }
        path.push(`${x},${y}`);
    }

    return path;
}

// Draw the grid and the player
function draw() {
    ctx.fillStyle = BLACK;
    ctx.fillRect(0, 0, canvas.width, canvas.height); // Fill background

    // Draw the grid
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const rectX = x * BLOCK_SIZE;
            const rectY = y * BLOCK_SIZE;
            const block = grid[y][x];

            // Determine the color based on the block type
            if (block === 1 && revealedBlocks.has(`${x},${y}`)) {
                ctx.fillStyle = RED; // Dangerous block
            } else if (block === 2 && revealedBlocks.has(`${x},${y}`)) {
                ctx.fillStyle = GREEN; // Goal
            } else if (block === 3 && revealedBlocks.has(`${x},${y}`)) {
                ctx.fillStyle = PURPLE; // Teleporter
            } else if (revealedBlocks.has(`${x},${y}`)) {
                ctx.fillStyle = WHITE; // Revealed regular block
            } else {
                ctx.fillStyle = DARK_GRAY; // Unrevealed block
            }

            ctx.fillRect(rectX, rectY, BLOCK_SIZE, BLOCK_SIZE);
            ctx.strokeStyle = GREEN;
            ctx.strokeRect(rectX, rectY, BLOCK_SIZE, BLOCK_SIZE);
        }
    }

    // Draw the player
    const playerRectX = playerPos[0] * BLOCK_SIZE;
    const playerRectY = playerPos[1] * BLOCK_SIZE;
    ctx.fillStyle = BLUE;
    ctx.fillRect(playerRectX, playerRectY, BLOCK_SIZE, BLOCK_SIZE);
}

// Handle key presses for movement
document.addEventListener('keydown', (e) => {
    if (gameOver) return;

    if (e.key === "ArrowUp" && playerPos[1] > 0) {
        playerPos[1]--;
    } else if (e.key === "ArrowDown" && playerPos[1] < GRID_SIZE - 1) {
        playerPos[1]++;
    } else if (e.key === "ArrowLeft" && playerPos[0] > 0) {
        playerPos[0]--;
    } else if (e.key === "ArrowRight" && playerPos[0] < GRID_SIZE - 1) {
        playerPos[0]++;
    }

    revealedBlocks.add(`${playerPos[0]},${playerPos[1]}`);
    checkBlock();
    updateUI();
    draw();
});

// Check the current block the player is on
function checkBlock() {
    const x = playerPos[0];
    const y = playerPos[1];
    const block = grid[y][x];

    if (block === 1 || block === 3) { // Dangerous block (red) or Teleporter (purple)
        // Reset player position to the first block after hitting dangerous block or teleporting
        playerPos = [0, 0];
        message = block === 1 ? "You hit a danger! Resetting position..." : "Teleported! Resetting position...";
    } else if (block === 2) { // True goal (green)
        gameOver = true;
        message = `You win! Time: ${(Date.now() - startTime) / 1000}s`;
    }
}

// Update the UI with lives and time
function updateUI() {
    document.getElementById("lives").textContent = gameMode === 'normal' ? `Lives: ${lives}` : `Lives: Unlimited (Speedrun)`;
    document.getElementById("timer").textContent = `Time: ${Math.floor((Date.now() - startTime) / 1000)}s`;
    document.getElementById("status").textContent = message || "Game On!";
}

// Restart the game
function restartGame() {
    initGame();
    gameOver = false;
}
