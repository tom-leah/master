import pygame
import sys
import random
import threading

pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Game With Targets")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Tank properties
tank_x = WIDTH // 2
tank_y = HEIGHT // 2
tank_speed = 5
tank_size = 40

# Bullets
bullets = []
bullet_speed = 10

# Targets
targets = []
TARGET_SIZE = 30
TARGET_SPAWN_TIME = 120  # frames
spawn_timer = 0

# Explosion animation
explosions = []  # each: [x, y, frame]
EXPLOSION_FRAMES = 10

# Score
score = 0
font = pygame.font.SysFont("Arial", 28)

# Benedict status and timer
benedict67 = False
timer_done = True

clock = pygame.time.Clock()
running = True


def spawn_target():
    x = random.randint(0, WIDTH - TARGET_SIZE)
    y = random.randint(0, HEIGHT - TARGET_SIZE)
    targets.append([x, y])

def set_variable():
    global timer_done
    timer_done = True

while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Fire bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([tank_x + tank_size // 2, tank_y])

    # Tank movement
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
    bullets = [b for b in bullets if b[1] > 0]

    # Spawn targets
    spawn_timer += 1
    if spawn_timer >= TARGET_SPAWN_TIME:
        spawn_target()
        spawn_timer = 0

    # Collision detection
    for bullet in bullets[:]:
        for target in targets[:]:
            if (
                    target[0] < bullet[0] < target[0] + TARGET_SIZE
                        and target[1] < bullet[1] < target[1] + TARGET_SIZE
            ):
                # Add explosion
                explosions.append([target[0], target[1], 0])

                # Remove target and bullet
                targets.remove(target)
                bullets.remove(bullet)

                # Score
                score += 10

                # Benedict Bad
                benedict67= True
                timer_done = False
                timer = threading.Timer(5.0, set_variable)  # 5.0 is the delay in seconds
                timer.start()

                break

    # Update explosion frames
    for explosion in explosions[:]:
        explosion[2] += 1
        if explosion[2] > EXPLOSION_FRAMES:
            explosions.remove(explosion)

    # Draw everything
    WIN.fill(WHITE)

    # Draw tank
    pygame.draw.rect(WIN, GREEN, (tank_x, tank_y, tank_size, tank_size))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, (*bullet, 5, 10))

    # Draw targets
    for target in targets:
        pygame.draw.rect(WIN, BLACK, (target[0], target[1], TARGET_SIZE, TARGET_SIZE))

    # Draw explosions (simple expanding yellow circle)
    for x, y, frame in explosions:
        radius = frame * 3
        pygame.draw.circle(WIN, YELLOW, (x + TARGET_SIZE // 2, y + TARGET_SIZE // 2), radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(score_text, (10, 10))

    # Draw benedict bad
    if benedict67 and not timer_done:
        benedict_text = font.render(f"Benedict 67!", True, BLACK)
        WIN.blit(benedict_text, (10, 40))

    pygame.display.update()
