import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 10
BLOCK_SIZE = SCREEN_WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
DARK_GRAY = (80, 80, 80)
BRIGHT_BLUE = (0, 102, 255)
BRIGHT_RED = (255, 0, 0)
BRIGHT_PURPLE = (153, 0, 255)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dig, Dig, Repeat")

# Initialize clock
clock = pygame.time.Clock()

# Generate the grid with one correct path, dangers, and Teleporteds
def generate_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    path = generate_path()

    # Add dangers to random blocks that are not on the path
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if random.random() < 0.2 and (x, y) not in path and (x, y) != (0, 0):
                grid[y][x] = 1  # Dangerous block

    # Add Teleporteds
    for _ in range(random.randint(3, 5)):  # Add 3-5 Teleporteds
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == 0 and (x, y) not in path and (x, y) != (GRID_SIZE - 1, GRID_SIZE - 1):
                grid[y][x] = 3  # Teleported
                break

    # Set the true goal
    grid[GRID_SIZE - 1][GRID_SIZE - 1] = 2  # True goal
    return grid

# Generate the correct path
def generate_path():
    path = []
    x, y = 0, 0
    path.append((x, y))

    while (x, y) != (GRID_SIZE - 1, GRID_SIZE - 1):
        if x < GRID_SIZE - 1 and y < GRID_SIZE - 1:
            if random.choice([True, False]):
                x += 1
            else:
                y += 1
        elif x < GRID_SIZE - 1:
            x += 1
        elif y < GRID_SIZE - 1:
            y += 1
        path.append((x, y))

    return path

# Draw the grid
def draw_grid(grid, player_pos, revealed_blocks):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

            if (x, y) == player_pos:
                pygame.draw.rect(screen, BRIGHT_BLUE, rect)  # Player
            elif (x, y) in revealed_blocks:
                if grid[y][x] == 2:
                    pygame.draw.rect(screen, BRIGHT_GREEN, rect)  # True goal
                elif grid[y][x] == 1:
                    pygame.draw.rect(screen, BRIGHT_RED, rect)  # Dangerous block
                elif grid[y][x] == 3:
                    pygame.draw.rect(screen, BRIGHT_PURPLE, rect)  # Teleported block
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Regular block (not visited yet)

            pygame.draw.rect(screen, DARK_GRAY, rect, 2)  # Grid lines

# Normal Game Loop
def normal_mode():
    grid = generate_grid()
    player_pos = [0, 0]
    revealed_blocks = set()  # To keep track of blocks revealed by the player
    lives = 3  # Start with 3 lives
    game_over = False
    message = ""

    # Start timer
    start_time = time.time()
    elapsed_time = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        if not game_over:
            # Handle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= 1
            if keys[pygame.K_DOWN] and player_pos[1] < GRID_SIZE - 1:
                player_pos[1] += 1
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= 1
            if keys[pygame.K_RIGHT] and player_pos[0] < GRID_SIZE - 1:
                player_pos[0] += 1

            # Add the current block to the revealed blocks set
            revealed_blocks.add(tuple(player_pos))

            # Check the current block
            current_block = grid[player_pos[1]][player_pos[0]]
            if current_block == 1:  # Dangerous block
                lives -= 1
                message = "You hit a danger!"
                player_pos = [0, 0]  # Reset to start
                if lives <= 0:
                    game_over = True
                    message = f"Game Over! Time: {elapsed_time} seconds"
            elif current_block == 3:  # Teleported
                lives -= 1
                message = "Teleported! Try again!"
                player_pos = [0, 0]  # Reset to start
                if lives <= 0:
                    game_over = True
                    message = f"Game Over! Time: {elapsed_time} seconds"
            elif current_block == 2:  # True goal
                elapsed_time = round(time.time() - start_time, 2)  # Get the time taken to reach the goal
                message = f"You win! Time: {elapsed_time} seconds"
                game_over = True

        # Draw the grid and the player
        draw_grid(grid, tuple(player_pos), revealed_blocks)

        # Display lives and messages
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, BRIGHT_GREEN)
        screen.blit(lives_text, (10, 10))
        message_text = font.render(message, True, BRIGHT_GREEN)
        screen.blit(message_text, (10, 50))

        # Game over message
        if game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("GAME OVER", True, BRIGHT_GREEN)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            restart_text = font.render("Press R to Restart", True, BRIGHT_GREEN)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                normal_mode()  # Restart the game

        pygame.display.flip()
        clock.tick(10)

# Speedrun Game Loop
def speedrun_mode():
    grid = generate_grid()
    player_pos = [0, 0]
    revealed_blocks = set()  # To keep track of blocks revealed by the player
    game_over = False
    message = ""

    # Start timer
    start_time = time.time()
    elapsed_time = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not game_over:
            # Handle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= 1
            if keys[pygame.K_DOWN] and player_pos[1] < GRID_SIZE - 1:
                player_pos[1] += 1
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= 1
            if keys[pygame.K_RIGHT] and player_pos[0] < GRID_SIZE - 1:
                player_pos[0] += 1

            # Add the current block to the revealed blocks set
            revealed_blocks.add(tuple(player_pos))

            # Check the current block
            current_block = grid[player_pos[1]][player_pos[0]]
            if current_block == 1:  # Dangerous block
                message = "You hit a danger!"
                player_pos = [0, 0]  # Reset to start
            elif current_block == 3:  # Teleported
                message = "Teleported! Try again!"
                player_pos = [0, 0]  # Reset to start
            elif current_block == 2:  # True goal
                elapsed_time = round(time.time() - start_time, 2)  # Get the time taken to reach the goal
                message = f"You win! Time: {elapsed_time} seconds"
                game_over = True

        # Draw the grid and the player
        draw_grid(grid, tuple(player_pos), revealed_blocks)

        # Display messages
        font = pygame.font.Font(None, 36)
        message_text = font.render(message, True, BRIGHT_GREEN)
        screen.blit(message_text, (10, 50))

        # Game over message
        if game_over:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("GAME OVER", True, BRIGHT_GREEN)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            restart_text = font.render("Press R to Restart", True, BRIGHT_GREEN)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 20))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                speedrun_mode()  # Restart the game

        pygame.display.flip()
        clock.tick(10)

# Main menu screen
def main_menu():
    while True:
        screen.fill(BLACK)

        # Draw menu buttons
        font = pygame.font.Font(None, 48)
        #title_text = font.render("Dig, Dig, Repeat", True, BRIGHT_GREEN)
        normal_mode_text = font.render("Normal Mode", True, BRIGHT_GREEN)
        speedrun_mode_text = font.render("Speedrun Mode", True, BRIGHT_GREEN)
        exit_text = font.render("Exit", True, BRIGHT_GREEN)

        # Position buttons
        #screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))
        screen.blit(normal_mode_text, (SCREEN_WIDTH // 2 - normal_mode_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(speedrun_mode_text, (SCREEN_WIDTH // 2 - speedrun_mode_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if Normal Mode is clicked
                if SCREEN_WIDTH // 2 - normal_mode_text.get_width() // 2 < mouse_x < SCREEN_WIDTH // 2 + normal_mode_text.get_width() // 2 and \
                   SCREEN_HEIGHT // 2 - 100 < mouse_y < SCREEN_HEIGHT // 2 - 100 + normal_mode_text.get_height():
                    normal_mode()  # Start Normal Mode

                # Check if Speedrun Mode is clicked
                elif SCREEN_WIDTH // 2 - speedrun_mode_text.get_width() // 2 < mouse_x < SCREEN_WIDTH // 2 + speedrun_mode_text.get_width() // 2 and \
                     SCREEN_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2 + speedrun_mode_text.get_height():
                    speedrun_mode()  # Start Speedrun Mode

                # Check if Exit is clicked
                elif SCREEN_WIDTH // 2 - exit_text.get_width() // 2 < mouse_x < SCREEN_WIDTH // 2 + exit_text.get_width() // 2 and \
                     SCREEN_HEIGHT // 2 + 100 < mouse_y < SCREEN_HEIGHT // 2 + 100 + exit_text.get_height():
                    pygame.quit()
                    return

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()  # Run the menu
