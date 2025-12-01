import pygame
import sys
import random
import threading
import math

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cartoony Tank Game")

# Colors (bright, cartoony)
WHITE = (255, 255, 255)
GREEN = (0, 220, 0)
GREEN_DARK = (0, 160, 0)
RED = (255, 80, 80)
ORANGE = (255, 150, 50)
YELLOW = (255, 240, 0)
BLACK = (0, 0, 0)
BLUE = (100, 160, 255)
BIRD_COLOR = (255, 255, 255)

# Tank properties
tank_x = WIDTH // 2
tank_y = HEIGHT // 2
tank_speed = 5
tank_size = 40

# Game state
alive = True

# Bullets
bullets = []
bullet_speed = 10

# Targets
targets = []
TARGET_SIZE = 30
TARGET_SPAWN_TIME = 120
spawn_timer = 0

# Birds
birds = []
BIRD_SIZE = 30
BIRD_SPAWN_TIME = 150
bird_timer = 0
BIRD_SPEED = 2.5

# Explosion animation
explosions = []   # each: [x, y, frame]
EXPLOSION_FRAMES = 10

# Score
score = 0
font = pygame.font.SysFont("Comic Sans MS", 28)  # Cartoon font

# Benedict status
benedict67 = False
timer_done = True

clock = pygame.time.Clock()
running = True


# ----------------------------
# HELPERS
# ----------------------------

def spawn_target():
    x = random.randint(0, WIDTH - TARGET_SIZE)
    y = random.randint(0, HEIGHT - TARGET_SIZE)
    targets.append([x, y])


def spawn_bird():
    """Spawn a bird at a random screen edge."""
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        x = random.randint(0, WIDTH - BIRD_SIZE)
        y = -BIRD_SIZE
    elif side == "bottom":
        x = random.randint(0, WIDTH - BIRD_SIZE)
        y = HEIGHT
    elif side == "left":
        x = -BIRD_SIZE
        y = random.randint(0, HEIGHT - BIRD_SIZE)
    else:
        x = WIDTH
        y = random.randint(0, HEIGHT - BIRD_SIZE)

    birds.append([x, y])


def respawn_tank():
    """Respawn tank in center."""
    global tank_x, tank_y, alive, score
    tank_x = WIDTH // 2
    tank_y = HEIGHT // 2
    alive = True
    score = 0


def set_variable():
    global timer_done
    timer_done = True


def draw_cartoon_tank(surface, x, y):
    body_rect = pygame.Rect(x, y, tank_size, tank_size)

    pygame.draw.rect(surface, GREEN, body_rect, border_radius=12)
    pygame.draw.rect(surface, GREEN_DARK, body_rect, width=3, border_radius=12)

    center_x = x + tank_size // 2
    center_y = y + tank_size // 2
    pygame.draw.circle(surface, GREEN_DARK, (center_x, center_y), 12)
    pygame.draw.circle(surface, BLACK, (center_x, center_y), 12, 2)

    pygame.draw.line(surface, GREEN_DARK, (center_x, center_y),
                     (center_x, center_y - 25), 6)


def draw_cartoon_target(surface, x, y):
    center = (x + TARGET_SIZE // 2, y + TARGET_SIZE // 2)
    r = TARGET_SIZE // 2

    pygame.draw.circle(surface, RED, center, r)
    pygame.draw.circle(surface, WHITE, center, r - 6)
    pygame.draw.circle(surface, RED, center, r - 12)
    pygame.draw.circle(surface, BLACK, center, r, 3)


def draw_cartoon_bullet(surface, x, y):
    pygame.draw.ellipse(surface, ORANGE, (x, y, 8, 14))
    pygame.draw.ellipse(surface, BLACK, (x, y, 8, 14), 2)


def draw_cartoon_explosion(surface, x, y, frame):
    size = frame * 4
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        end_x = x + TARGET_SIZE//2 + math.cos(rad) * size
        end_y = y + TARGET_SIZE//2 + math.sin(rad) * size
        pygame.draw.line(surface, YELLOW,
                         (x + TARGET_SIZE//2, y + TARGET_SIZE//2),
                         (end_x, end_y), 4)


def draw_bird(surface, x, y):
    """Simple white bird shape."""
    pygame.draw.ellipse(surface, BIRD_COLOR, (x, y, BIRD_SIZE, BIRD_SIZE // 2))
    pygame.draw.polygon(surface, BIRD_COLOR,
                        [(x + BIRD_SIZE // 2, y),
                         (x + BIRD_SIZE, y + BIRD_SIZE // 4),
                         (x + BIRD_SIZE // 2, y + BIRD_SIZE // 2)])


# ----------------------------
# MAIN LOOP
# ----------------------------

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Fire bullet
        if event.type == pygame.KEYDOWN and alive:
            if event.key == pygame.K_SPACE:
                bullets.append([tank_x + tank_size//2 - 4, tank_y])

    if alive:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and tank_x > 0:
            tank_x -= tank_speed
        if keys[pygame.K_RIGHT] and tank_x < WIDTH - tank_size:
            tank_x += tank_speed
        if keys[pygame.K_UP] and tank_y > 0:
            tank_y -= tank_speed
        if keys[pygame.K_DOWN] and tank_y < HEIGHT - tank_size:
            tank_y += tank_speed

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets = [b for b in bullets if b[1] > -20]

    # Spawn targets
    spawn_timer += 1
    if spawn_timer >= TARGET_SPAWN_TIME:
        spawn_target()
        spawn_timer = 0

    # Spawn birds
    bird_timer += 1
    if bird_timer >= BIRD_SPAWN_TIME:
        spawn_bird()
        bird_timer = 0

    # Move birds toward tank
    for bird in birds:
        dx = tank_x - bird[0]
        dy = tank_y - bird[1]
        dist = math.hypot(dx, dy)

        if dist != 0:
            bird[0] += (dx / dist) * BIRD_SPEED
            bird[1] += (dy / dist) * BIRD_SPEED

    # Bird kills tank
    for bird in birds:
        if alive and abs(bird[0] - tank_x) < BIRD_SIZE and abs(bird[1] - tank_y) < BIRD_SIZE:
            alive = False
            respawn_tank()

    # Bullet collisions
    for bullet in bullets[:]:
        for target in targets[:]:
            if target[0] < bullet[0] < target[0] + TARGET_SIZE and \
               target[1] < bullet[1] < target[1] + TARGET_SIZE:

                explosions.append([target[0], target[1], 0])
                bullets.remove(bullet)
                targets.remove(target)
                score += 10

                benedict67 = True
                timer_done = False
                threading.Timer(5.0, set_variable).start()

                break

    # Update explosions
    for explosion in explosions[:]:
        explosion[2] += 1
        if explosion[2] > EXPLOSION_FRAMES:
            explosions.remove(explosion)

    # Draw scene
    WIN.fill(BLUE)

    if alive:
        draw_cartoon_tank(WIN, tank_x, tank_y)

    for bullet in bullets:
        draw_cartoon_bullet(WIN, bullet[0], bullet[1])

    for target in targets:
        draw_cartoon_target(WIN, target[0], target[1])

    for x, y, frame in explosions:
        draw_cartoon_explosion(WIN, x, y, frame)

    for bird in birds:
        draw_bird(WIN, bird[0], bird[1])

    score_text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(score_text, (10, 10))

    if benedict67 and not timer_done:
        benedict_text = font.render("Benedict 67!", True, BLACK)
        WIN.blit(benedict_text, (10, 50))

    pygame.display.update()
