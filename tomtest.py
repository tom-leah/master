import pygame
import pygame.gfxdraw
import random
import sys

# =========================
#   SUPER COMPLEX SNAKE - Cartoon Graphics
# =========================

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE = 20
GRID_W = WIDTH // TILE
GRID_H = HEIGHT // TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 24)

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
        # ensure fruit doesn't spawn outside grid
        self.pos = random_grid_pos()
        self.type = type

# =========================
# Moving Obstacles
# =========================
class Obstacle:
    def __init__(self):
        self.pos = random_grid_pos()
        self.direction = random.choice([[1,0],[-1,0],[0,1],[0,-1]])

    def move(self):
        self.pos[0] = (self.pos[0] + self.direction[0]) % GRID_W
        self.pos[1] = (self.pos[1] + self.direction[1]) % GRID_H

# =========================
# Cartoon-Style Renderers
# =========================

def draw_snake(screen, snake, TILE):
    """Draw snake as rounded circles with a head that has eyes."""
    for i, part in enumerate(snake.body):
        x = part[0] * TILE
        y = part[1] * TILE

        # Body color (slightly brighter for head)
        if i == 0:
            base_color = (0, 220, 0)
            outline_color = (0, 180, 0)
            radius = TILE//2 - 1
        else:
            base_color = (0, 200, 0)
            outline_color = (0, 150, 0)
            radius = TILE//2 - 2

        # Anti-aliased filled circle for smooth body
        pygame.gfxdraw.filled_circle(screen, x + TILE//2, y + TILE//2, radius, base_color)
        pygame.gfxdraw.aacircle(screen, x + TILE//2, y + TILE//2, radius, outline_color)

        # Head features
        if i == 0:
            # Eyes: positions scale with TILE
            eye_x_offset = max(3, TILE//6)
            eye_y_offset = max(3, TILE//8)
            eye_radius = max(1, TILE//10)
            # white of eye
            pygame.gfxdraw.filled_circle(screen, x + TILE//2 - eye_x_offset, y + TILE//2 - eye_y_offset, eye_radius+1, (255,255,255))
            pygame.gfxdraw.filled_circle(screen, x + TILE//2 + eye_x_offset, y + TILE//2 - eye_y_offset, eye_radius+1, (255,255,255))
            # pupil
            pygame.gfxdraw.filled_circle(screen, x + TILE//2 - eye_x_offset, y + TILE//2 - eye_y_offset, eye_radius, (0,0,0))
            pygame.gfxdraw.filled_circle(screen, x + TILE//2 + eye_x_offset, y + TILE//2 - eye_y_offset, eye_radius, (0,0,0))
            # small smile
            mouth_rect = pygame.Rect(x + TILE//2 - TILE//6, y + TILE//2, TILE//3, TILE//6)
            pygame.draw.arc(screen, (0,0,0), mouth_rect, 3.2, 6.1, 1)

def draw_fruit(screen, fruit, TILE):
    """Draw fruit as shaded circle, highlight and small leaf (cartoon)."""
    x = fruit.pos[0] * TILE
    y = fruit.pos[1] * TILE

    colors = {
        "normal": (255, 60, 60),
        "big": (255, 140, 0),
        "slow": (60, 60, 255),
        "speed": (255, 0, 255)
    }

    base_color = colors.get(fruit.type, (255, 0, 0))

    radius = TILE//2 - 1
    cx = x + TILE//2
    cy = y + TILE//2

    # Main fruit body
    pygame.gfxdraw.filled_circle(screen, cx, cy, radius, base_color)
    pygame.gfxdraw.aacircle(screen, cx, cy, radius, base_color)

    # Simple shading: darker bottom
    shadow_color = tuple(max(0, c - 50) for c in base_color)
    pygame.gfxdraw.filled_circle(screen, cx, cy + radius//3, radius//2, shadow_color)

    # Highlight (small white circle)
    highlight_r = max(2, TILE//8)
    pygame.gfxdraw.filled_circle(screen, cx - radius//2 + 2, cy - radius//2 + 2, highlight_r, (255,255,255))

    # Leaf (ellipse)
    leaf_w = max(4, TILE//4)
    leaf_h = max(6, TILE//3)
    leaf_rect = pygame.Rect(cx + radius//2 - 2, cy - radius//2, leaf_w, leaf_h)
    pygame.draw.ellipse(screen, (50,180,50), leaf_rect)
    pygame.draw.ellipse(screen, (10,100,10), leaf_rect, 1)

def draw_obstacle(screen, obs, TILE):
    x = obs.pos[0] * TILE
    y = obs.pos[1] * TILE

    base_color = (150,150,150)

    # Cartoon rock (circle)
    pygame.gfxdraw.filled_circle(screen, x + TILE//2, y + TILE//2, TILE//2 - 2, base_color)
    pygame.gfxdraw.aacircle(screen, x + TILE//2, y + TILE//2, TILE//2 - 2, base_color)

    # Face (eyes)
    pygame.gfxdraw.filled_circle(screen, x + TILE//2 - 4, y + TILE//2 - 3, 2, (0,0,0))
    pygame.gfxdraw.filled_circle(screen, x + TILE//2 + 4, y + TILE//2 - 3, 2, (0,0,0))

    # Mouth (frown)
    pygame.draw.arc(
        screen, (0,0,0),
        (x + TILE//2 - 5, y + TILE//2 - 1, 10, 8),
        3.4, 5.9, 2
    )


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

        # Handle Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != [0,1]:
                    snake.buffer.append([0,-1])
                if event.key == pygame.K_DOWN and snake.direction != [0,-1]:
                    snake.buffer.append([0,1])
                if event.key == pygame.K_LEFT and snake.direction != [1,0]:
                    snake.buffer.append([-1,0])
                if event.key == pygame.K_RIGHT and snake.direction != [-1,0]:
                    snake.buffer.append([1,0])

        snake.move()

        # Collision with self
        if snake.collide_self():
            return  # exit game loop → restart

        # Obstacle movement & collision
        for obs in obstacles:
            obs.move()
            if snake.body[0] == obs.pos:
                return

        # Fruit collision
        for f in list(fruits):
            if snake.body[0] == f.pos:
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

        # Draw
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
        main()  # run game
        # Game Over screen
        screen.fill((0,0,0))
        msg = FONT.render("Game Over! Press SPACE to restart.", True, (255,255,255))
        screen.blit(msg, (200, 260))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False


