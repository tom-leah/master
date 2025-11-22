"""
Classic Snake game using Pygame.

Controls:
 - Arrow keys or WASD to move.
 - R to restart after game over.
 - Esc or close window to quit.

"""

import pygame
import random
import sys

# --------- Configuration ----------
CELL_SIZE = 20         # size of a grid cell in pixels
GRID_WIDTH = 30        # number of cells horizontally
GRID_HEIGHT = 20       # number of cells vertically
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

FPS = 5               # base frames per second (speed of the snake)
SPEED_INCREMENT = 0.5  # speed increase each time snake eats food
MAX_FPS = 30

# Colors (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 180, 0)
RED = (200, 30, 30)
YELLOW = (235, 200, 20)
BLUE = (0, 120, 200)

# ---------------------------------

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def clamp(val, minv, maxv):
    return max(minv, min(maxv, val))

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.large_font = pygame.font.SysFont(None, 56)
        self.reset()

    def reset(self):
        # Start snake in the center, length 3, moving right
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = [(start_x - i, start_y) for i in range(3)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.spawn_food()
        self.score = 0
        self.fps = FPS
        self.game_over = False

    def spawn_food(self):
        # spawn in an empty cell
        empty_cells = {(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)} - set(self.snake)
        if not empty_cells:
            self.food = None
            return
        self.food = random.choice(list(empty_cells))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if self.direction != DOWN:
                        self.next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.direction != UP:
                        self.next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.direction != RIGHT:
                        self.next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.direction != LEFT:
                        self.next_direction = RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self):
        if self.game_over:
            return

        # apply next direction (prevents reversing into itself)
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check collisions with walls
        nx, ny = new_head
        if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
            self.game_over = True
            return

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food
        if self.food and new_head == self.food:
            self.score += 1
            self.spawn_food()
            # speed up slightly
            self.fps = clamp(self.fps + SPEED_INCREMENT, FPS, MAX_FPS)
        else:
            # remove tail
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)

        # Optionally draw grid
        self.draw_grid()

        # Draw food
        if self.food:
            fx, fy = self.food
            rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, RED, rect)

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # head a different color
            if i == 0:
                pygame.draw.rect(self.screen, BLUE, rect)
                # small eye/shine on head for visual
                eye_size = CELL_SIZE // 6
                eye_x = rect.x + CELL_SIZE // 2 - eye_size // 2 + (self.direction[0] * eye_size)
                eye_y = rect.y + CELL_SIZE // 2 - eye_size // 2 + (self.direction[1] * eye_size)
                pygame.draw.rect(self.screen, WHITE, (eye_x, eye_y, eye_size, eye_size))
            else:
                pygame.draw.rect(self.screen, GREEN, rect)

        # Draw score
        score_surf = self.font.render(f"Score: {self.score}", True, YELLOW)
        self.screen.blit(score_surf, (8, 8))

        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))  # semi-transparent
            self.screen.blit(overlay, (0, 0))

            text = self.large_font.render("Game Over", True, WHITE)
            sub = self.font.render("Press R to restart or Esc to quit", True, WHITE)

            txt_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 24))
            self.screen.blit(text, txt_rect)
            self.screen.blit(sub, sub_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            # Use integer tick based on current fps
            self.clock.tick(self.fps)

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
