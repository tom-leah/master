# Updated Snake game with multiple food colors and special red food death explosion
# (Full rewritten version based on user's original code)

import pygame
import random
import sys

# --------- Configuration ----------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

FPS = 7
MAX_FPS = 30
SPEED_INCREMENT = 0.3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
GREEN = (0, 180, 0)
RED = (200, 30, 30)
YELLOW = (235, 200, 20)
BLUE = (0, 120, 200)
ORANGE = (255, 155, 0)
PURPLE = (160, 60, 200)

# Food types
FOOD_COLORS = [GREEN, YELLOW, ORANGE, PURPLE, RED]  # red = deadly
NUM_FOOD = 6

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def clamp(val, minv, maxv):
    return max(minv, min(maxv, val))


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake - Multi Food")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.large_font = pygame.font.SysFont(None, 56)
        self.reset()

    def reset(self):
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = [(start_x - i, start_y) for i in range(3)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.fps = FPS
        self.food_items = []
        self.spawn_multiple_food()
        self.game_over = False
        self.death_explosion = []

    def spawn_multiple_food(self):
        self.food_items.clear()
        empty = list({(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)} - set(self.snake))
        random.shuffle(empty)
        for i in range(NUM_FOOD):
            pos = empty[i]
            color = random.choice(FOOD_COLORS)
            self.food_items.append((pos, color))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.direction != DOWN:
                        self.next_direction = UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.direction != UP:
                        self.next_direction = DOWN
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.direction != RIGHT:
                        self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.direction != LEFT:
                        self.next_direction = RIGHT
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        nx, ny = new_head
        if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
            self.trigger_explosion()
            return

        if new_head in self.snake:
            self.trigger_explosion()
            return

        self.snake.insert(0, new_head)

        ate = None
        for (pos, color) in self.food_items:
            if pos == new_head:
                ate = (pos, color)
                break

        if ate:
            pos, color = ate
            if color == RED:
                self.trigger_explosion()
                return
            else:
                self.score += 1
                self.fps = clamp(self.fps + SPEED_INCREMENT, FPS, MAX_FPS)
                self.food_items.remove(ate)
                self.spawn_new_food()
        else:
            self.snake.pop()

    def spawn_new_food(self):
        empty = list({(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)} - set(self.snake) - {p for p, c in self.food_items})
        if empty:
            pos = random.choice(empty)
            color = random.choice(FOOD_COLORS)
            self.food_items.append((pos, color))

    def trigger_explosion(self):
        self.game_over = True
        self.death_explosion = [(pos, color) for (pos, color) in self.food_items]

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        # Draw all food
        for (pos, color) in self.food_items:
            x, y = pos
            pygame.draw.rect(self.screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(self.screen, BLUE, rect)
            else:
                pygame.draw.rect(self.screen, GREEN, rect)

        # Explosion (food scattering effect)
        if self.game_over:
            for (pos, color) in self.death_explosion:
                x, y = pos
                pygame.draw.circle(self.screen, color, (x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2)

            text = self.large_font.render("pawsome", True, WHITE)
            rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text, rect)

            sub = self.font.render("Press R to restart", True, WHITE)
            sub_r = sub.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
            self.screen.blit(sub, sub_r)

        # Score
        score_surf = self.font.render(f"Score: {self.score}", True, YELLOW)
        self.screen.blit(score_surf, (8, 8))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)


def main():
    SnakeGame().run()


if __name__ == "__main__":
    main()
