import pygame
import pygame.gfxdraw
import random
import sys

# =========================
#   REALISTIC SNAKE GAME
# =========================

pygame.init()

WIDTH, HEIGHT = 1200, 900
TILE = 20
GRID_W = WIDTH // TILE
GRID_H = HEIGHT // TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Times", 30, bold=True, italic=False)


# =========================
# Helper Functions
# =========================
def random_grid_pos():
    return [random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1)]


# =========================
# Snake Class
# =========================
class Snake:
    def __init__(self):
        self.body = [[GRID_W // 2, GRID_H // 2]]
        self.direction = [1, 0]
        self.length = 5
        self.speed = 8
        self.buffer = []

    def move(self):
        if self.buffer:
            self.direction = self.buffer.pop(0)

        head = [
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1]
        ]

        # Wrap-around
        head[0] %= GRID_W
        head[1] %= GRID_H

        self.body.insert(0, head)

        if len(self.body) > self.length:
            self.body.pop()

    def collide_self(self):
        return self.body[0] in self.body[1:]


# =========================
# Fruits & Power-ups
# =========================
class Fruit:
    def __init__(self, type="normal"):
        self.pos = random_grid_pos()
        self.type = type


# =========================
# Moving Obstacles
# =========================
class Obstacle:
    def __init__(self):
        self.pos = random_grid_pos()
        self.direction = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])

    def move(self):
        self.pos[0] = (self.pos[0] + self.direction[0]) % GRID_W
        self.pos[1] = (self.pos[1] + self.direction[1]) % GRID_H


# =========================
# REALISTIC SNAKE RENDERER
# =========================
def draw_snake(screen, snake, TILE):
    """Realistic smooth snake with shading + tapered tail."""
    for i, part in enumerate(snake.body):

        x = part[0] * TILE
        y = part[1] * TILE

        # Realistic gradient: head bright → tail darker
        shade = max(40, 200 - i * 2)
        color = (0, shade, 0)

        cx = x + TILE // 2
        cy = y + TILE // 2

        # Natural taper (head largest)
        radius = max(4, TILE // 2 - i // 18)

        # Main body
        pygame.gfxdraw.filled_circle(screen, cx, cy, radius, color)
        pygame.gfxdraw.aacircle(screen, cx, cy, radius, color)

        # Highlight for shiny snake skin
        highlight = (
            min(color[0] + 40, 255),
            min(color[1] + 40, 255),
            min(color[2] + 40, 255)
        )

        pygame.gfxdraw.filled_circle(
            screen,
            cx - radius // 2,
            cy - radius // 3,
            max(2, radius // 3),
            highlight
        )

        # Lower shadow shading
        shadow = (
            max(color[0] - 50, 0),
            max(color[1] - 50, 0),
            max(color[2] - 50, 0)
        )

        pygame.gfxdraw.filled_circle(
            screen,
            cx + radius // 3,
            cy + radius // 4,
            max(2, radius // 2),
            shadow
        )


# =========================
# Fruit Renderer
# =========================
def draw_fruit(screen, fruit, TILE):
    x = fruit.pos[0] * TILE
    y = fruit.pos[1] * TILE

    colors = {
        "normal": (255, 60, 60),
        "big": (255, 140, 0),
        "slow": (60, 60, 255),
        "speed": (255, 0, 255)
    }

    base_color = colors.get(fruit.type, (255, 0, 0))

    radius = TILE // 2 - 1
    cx = x + TILE // 2
    cy = y + TILE // 2

    pygame.gfxdraw.filled_circle(screen, cx, cy, radius, base_color)
    pygame.gfxdraw.aacircle(screen, cx, cy, radius, base_color)

    # Shadow
    shadow_color = tuple(max(0, c - 50) for c in base_color)
    pygame.gfxdraw.filled_circle(screen, cx, cy + radius // 3, radius // 2, shadow_color)

    # Highlight
    pygame.gfxdraw.filled_circle(screen, cx - 4, cy - 4, radius // 4, (255, 255, 255))


# =========================
# Obstacle Renderer
# =========================
def draw_obstacle(screen, obs, TILE):
    x = obs.pos[0] * TILE
    y = obs.pos[1] * TILE

    base_color = (150, 150, 150)

    pygame.gfxdraw.filled_circle(screen, x + TILE // 2, y + TILE // 2, TILE // 2 - 2, base_color)
    pygame.gfxdraw.aacircle(screen, x + TILE // 2, y + TILE // 2, TILE // 2 - 2, base_color)


# =========================
# Respawn Helper
# =========================
def respawn_snake(snake):
    snake.body = [[GRID_W // 2, GRID_H // 2]]
    snake.length = 5
    snake.direction = [1, 0]
    snake.speed = 8
    snake.buffer.clear()


# =========================
# Main Game Loop
# =========================
def main():
    snake = Snake()
    fruits = [Fruit(random.choice(["normal", "big", "slow", "speed"])) for _ in range(3)]
    obstacles = [Obstacle() for _ in range(5)]
    score = 0

    while True:
        clock.tick(10)

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != [0, 1]:
                    snake.buffer.append([0, -1])
                if event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                    snake.buffer.append([0, 1])
                if event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                    snake.buffer.append([-1, 0])
                if event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                    snake.buffer.append([1, 0])

        snake.move()

        # Collision with self
        if snake.collide_self():
            return

        # Obstacle collision
        for obs in obstacles:
            obs.move()
            if snake.body[0] == obs.pos:
                return

        # Fruit collision
        for f in list(fruits):
            if snake.body[1] == f.pos:

                if f.type == "normal":
                    snake.length += 1
                    score += 1
                elif f.type == "big":
                    snake.length += 3
                    score += 5
                elif f.type == "slow":
                    snake.speed = max(4, snake.speed - 2)
                elif f.type == "speed":
                    snake.speed += 2

                fruits.remove(f)
                fruits.append(Fruit(random.choice(["normal", "big", "slow", "speed"])))

        # Draw frame
        screen.fill((20, 20, 20))
        draw_snake(screen, snake, TILE)

        for f in fruits:
            draw_fruit(screen, f, TILE)
        for obs in obstacles:
            draw_obstacle(screen, obs, TILE)

        score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


# =========================
# Restart Loop
# =========================
if __name__ == "__main__":
    while True:
        main()
        screen.fill((0, 0, 0))
        msg = FONT.render("Game Over! Press SPACE to restart.", True, (255, 255, 255))
        screen.blit(msg, (200, 260))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
