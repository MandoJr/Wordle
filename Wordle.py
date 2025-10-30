import pygame
import sys
import random
import string

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_MAP = {
    "green": (83, 141, 78),
    "yellow": (181, 159, 59),
    "gray": (58, 58, 60)
}

# Grid settings
ROWS, COLS = 6, 5
BOX_SIZE = 70
GAP = 10
START_X = (WIDTH - (COLS * (BOX_SIZE + GAP) - GAP)) // 2
START_Y = 100

# Font setup
pygame.font.init()
font = pygame.font.SysFont("arial", 48, bold=True)

# Load words from file
try:
    with open("words.txt") as f:
        words = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    # fallback if file not found
    words = ["apple", "grape", "peach", "berry", "mango"]

# Function to start/restart a game
def start_game():
    secret_word = random.choice(words).upper()
    grid_state = [["" for _ in range(COLS)] for _ in range(ROWS)]
    colors_state = [["gray" for _ in range(COLS)] for _ in range(ROWS)]
    return secret_word, grid_state, colors_state

# Initialize game
secret = random.choice(words).upper()
grid = [["" for _ in range(COLS)] for _ in range(ROWS)]
colors_grid = [["gray" for _ in range(COLS)] for _ in range(ROWS)]
current_row = 0
current_col = 0
game_over = False
message = ""
secret = random.choice(words).upper()
print("Secret word (for testing):", secret)  # remove later

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if current_col > 0:
                    current_col -= 1
                    grid[current_row][current_col] = ""
            elif event.key == pygame.K_RETURN:
                if current_col == COLS:
                    # Build the guessed word
                    guess = "".join(grid[current_row])

                    # Step 1: handle duplicate letters correctly
                    colors = ["gray"] * COLS
                    secret_letters = list(secret)

                    # Mark greens
                    for i in range(COLS):
                        if guess[i] == secret[i]:
                            colors[i] = "green"
                            secret_letters[i] = None

                    # Mark yellows
                    for i in range(COLS):
                        if colors[i] != "green" and guess[i] in secret_letters:
                            colors[i] = "yellow"
                            secret_letters[secret_letters.index(guess[i])] = None

                    # Store colors in colors_grid
                    colors_grid[current_row] = colors

                    # Check win
                    if guess == secret:
                        game_over = True
                        message = "You Win!"
                    else:
                        current_row += 1
                        current_col = 0
                        if current_row >= ROWS:
                            game_over = True
                            message = f"Game Over! Word was {secret}"
            elif event.unicode in string.ascii_letters and current_col < COLS:
                grid[current_row][current_col] = event.unicode.upper()
                current_col += 1

        # Restart game when over
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                secret, grid, colors_grid = start_game()
                current_row = 0
                current_col = 0
                game_over = False
                message = ""
                print("Secret word (for testing):", secret)  # remove later

    # Draw background
    screen.fill(BLACK)

    # Draw grid and letters
    for row in range(ROWS):
        for col in range(COLS):
            x = START_X + col * (BOX_SIZE + GAP)
            y = START_Y + row * (BOX_SIZE + GAP)
            # Draw box color
            pygame.draw.rect(screen, COLOR_MAP[colors_grid[row][col]], (x, y, BOX_SIZE, BOX_SIZE))
            # Draw border
            pygame.draw.rect(screen, WHITE, (x, y, BOX_SIZE, BOX_SIZE), 3)
            # Draw letter
            letter = grid[row][col]
            if letter:
                text_surface = font.render(letter, True, WHITE)
                text_rect = text_surface.get_rect(center=(x + BOX_SIZE//2, y + BOX_SIZE//2))
                screen.blit(text_surface, text_rect)

    # Draw win/lose message
    if game_over:
        msg_surface = font.render(message, True, WHITE)
        msg_rect = msg_surface.get_rect(center=(WIDTH//2, HEIGHT - 50))
        screen.blit(msg_surface, msg_rect)
        # Draw restart instruction
        restart_surface = pygame.font.SysFont("arial", 24, bold=True).render("Press R to Restart", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WIDTH//2, HEIGHT - 20))
        screen.blit(restart_surface, restart_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
