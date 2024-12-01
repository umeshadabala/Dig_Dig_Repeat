# Dig, Dig, Repeat - Game

## Overview

"Dig, Dig, Repeat" is a grid-based, interactive game where the player navigates through a maze, avoiding dangers and teleporters, with the ultimate goal of reaching the designated "True Goal" block. The game features two modes: **Normal Mode** and **Speedrun Mode**. The player must carefully navigate the grid, uncovering hidden dangers and paths while racing against the clock in Speedrun Mode or managing lives in Normal Mode.

## Features

- **Two Game Modes**: 
  - **Normal Mode**: The player has 3 lives. If the player hits a dangerous block (red) or a teleporter (purple), they are reset to the starting position.
  - **Speedrun Mode**: The player has unlimited lives and tries to reach the True Goal block as quickly as possible.

- **Interactive Grid**: 
  - The grid contains dangerous blocks, teleporters, and the True Goal block, which the player needs to reach.
  - The grid is randomly generated each time you play.

- **Timer and Score**: 
  - Time is tracked, and the goal is to reach the True Goal in the fastest time (Speedrun Mode).
  - In Normal Mode, players must be careful not to run out of lives while trying to reach the True Goal.

- **Responsive UI**:
  - The UI shows the number of lives remaining (in Normal Mode), elapsed time, and the game status (e.g., if the player wins or loses).

## Installation

1. Clone or download this repository to your local machine.
2. Open the 'web' folder and `index.html` file in your browser to play the game.

## How to Play

### 1. Main Menu:
When you start the game, you will be presented with a **Main Menu**. From here, you can select between two game modes:
- **Normal Mode**: Requires the player to avoid dangerous blocks (red) and teleporters (purple) while trying to reach the True Goal (green). The player has 3 lives.
- **Speedrun Mode**: The player has unlimited lives and must reach the True Goal (green) as quickly as possible.

### 2. Gameplay:
- Use the arrow keys (`Up`, `Down`, `Left`, `Right`) to move the player through the grid.
- The player starts at the top-left corner of the grid (position `[0,0]`).
- The objective is to reach the **True Goal** block (green) while avoiding **Dangerous Blocks** (red) and **Teleporters** (purple).
- If the player encounters a **Dangerous Block** (red) or a **Teleporter** (purple), they are reset to the starting position `[0, 0]`.
- Once the player reaches the True Goal block (green), the game ends, and the time taken is displayed (Speedrun Mode).

### 3. UI Elements:
- **Lives**: Displays the number of lives remaining (Normal Mode only).
- **Timer**: Tracks the time spent in the game (Speedrun Mode or Normal Mode).
- **Status**: Displays the current game message, such as when the player hits a danger, teleports, or wins the game.

### 4. Restarting the Game:
- You can restart the game by clicking the "Restart" button in the game screen, or simply return to the **Main Menu** to start a new game.

## How It Works

### **Game Logic**:
- The game is built using **HTML**, **CSS**, and **JavaScript**.
- The grid is randomly generated at the start of each game, and the player must navigate it.
- The game features random placement of **Dangerous Blocks**, **Teleporters**, and the **True Goal**.
- Movement is controlled using arrow keys, and each block's type is checked to update the player's state.
- In **Speedrun Mode**, the game tracks the time taken to complete the game, with the goal of achieving the fastest time.
- In **Normal Mode**, the player has 3 lives and must avoid hitting Dangerous Blocks or Teleporters.

### **Grid Generation**:
- The grid is created dynamically in JavaScript, where each cell in the grid is either empty, a dangerous block, a teleporter, or the True Goal block.
- The player moves across the grid by interacting with the arrow keys, and the current position is updated as the player moves.

### **UI Rendering**:
- The game uses the **Canvas API** to draw the grid, player, and other UI elements like lives and timer.
- CSS styles are used to create the **terminal-themed UI** with green and black colors to give it a retro look.
- The game screen is updated continuously, and the player's position is redrawn after every move.

## Technologies Used

- **HTML5**: Used for the basic structure of the game.
- **CSS3**: Used for styling the game interface and making it responsive.
- **JavaScript**: Used for handling the game logic, grid generation, movement, and player interaction.

## Credits

- **Developer**: [Umesh Sriraj Adabala]
- **Special Thanks**: [Level Devil Game on poki.com]

## License

This project is open-source and licensed under the [MIT License](LICENSE).

---

Enjoy playing "Dig, Dig, Repeat"! Challenge yourself to beat your time and reach the True Goal as quickly as possible in **Speedrun Mode** or try to survive in **Normal Mode**! 🕹️
