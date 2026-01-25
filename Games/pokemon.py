import pygame
import sys
import random

# ----------------- Setup -----------------
pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cartoon Flappy Bird")

CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32, bold=True)
BIG_FONT = pygame.font.SysFont("Comic Sans MS", 60, bold=True)

# Bird settings
bird_x = 80
bird_y = HEIGHT // 2
bird_vel = 0
gravity = 0.3
flap_strength = -8

# Pipes
pipe_width = 70
pipe_gap = 250
pipe_speed = 3
pipes = []
spawn_timer = 0

score = 0
dead = False
death_timer = 0

# Colors
SKY_TOP = (135, 206, 250)
SKY_BOTTOM = (180, 230, 255)
PIPE_GREEN = (50, 220, 90)
PIPE_OUTLINE = (0, 140, 40)
GROUND_COLOR = (240, 200, 90)


def reset_game():
    global bird_y, bird_vel, pipes, score, dead, death_timer
    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes.clear()
    score = 0
    dead = False
    death_timer = 0


def spawn_pipe():
    gap_y = random.randint(100, HEIGHT - 200)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, gap_y)
    bottom_rect = pygame.Rect(WIDTH, gap_y + pipe_gap, pipe_width, HEIGHT - (gap_y + pipe_gap))
    return (top_rect, bottom_rect)


def draw_gradient(surface, color_top, color_bottom):
    """Cartoon sky gradient."""
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, i), (WIDTH, i))


# ----------------- Main Loop -----------------
while True:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dead:
                bird_vel = flap_strength
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # ----------------- Death Screen -----------------
    if dead:
        death_timer += 1
        draw_gradient(WIN, (255, 120, 120), (255, 80, 80))

        text = BIG_FONT.render("AGNES BAD", True, (255, 255, 255))
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2,
                        HEIGHT // 2 - text.get_height() // 2))

        pygame.display.update()

        if death_timer > 90:
            reset_game()

        continue

    # ----------------- Bird physics -----------------
    bird_vel += gravity
    bird_y += bird_vel

    # ----------------- Pipe spawning -----------------
    spawn_timer += 1
    if spawn_timer > 90:
        spawn_timer = 0
        pipes.append(spawn_pipe())

    # Move pipes + scoring
    for p in pipes:
        p[0].x -= pipe_speed
        p[1].x -= pipe_speed

        # Score when pipe passes bird
        if p[0].x + pipe_width == bird_x:
            score += 10

    # Delete offscreen pipes
    pipes = [p for p in pipes if p[0].x > -pipe_width]

    # Collision rectangles
    bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)

    # ----------------- Collisions -----------------
    if bird_y <= 0 or bird_y >= HEIGHT - 40:
        dead = True

    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            dead = True

    # ----------------- Draw everything -----------------
    draw_gradient(WIN, SKY_TOP, SKY_BOTTOM)

    # Ground
    pygame.draw.rect(WIN, GROUND_COLOR, (0, HEIGHT - 40, WIDTH, 40))

    # Cartoon Bird: body + eye + outline
    pygame.draw.circle(WIN, (255, 255, 0), (bird_x + 15, int(bird_y + 15)), 15)
    pygame.draw.circle(WIN, (0, 0, 0), (bird_x + 15, int(bird_y + 15)), 15, 3)

    # Eye
    pygame.draw.circle(WIN, (255, 255, 255), (bird_x + 22, int(bird_y + 10)), 6)
    pygame.draw.circle(WIN, (0, 0, 0), (bird_x + 23, int(bird_y + 10)), 3)

    # Beak
    pygame.draw.polygon(WIN, (255, 150, 0), [
        (bird_x + 30, bird_y + 18),
        (bird_x + 45, bird_y + 20),
        (bird_x + 30, bird_y + 25),
    ])

    # Draw pipes (cartoon style)
    for top, bottom in pipes:
        pygame.draw.rect(WIN, PIPE_GREEN, top)
        pygame.draw.rect(WIN, PIPE_GREEN, bottom)
        pygame.draw.rect(WIN, PIPE_OUTLINE, top, 4)
        pygame.draw.rect(WIN, PIPE_OUTLINE, bottom, 4)

    # Score (cartoon text)
    score_text = FONT.render(str(score), True, (0, 0, 0))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    # Update screen
    pygame.display.update()
