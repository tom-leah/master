import pygame
import sys
import random

# ----------------- Setup -----------------
pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)
BIG_FONT = pygame.font.SysFont("Arial", 60)

# Bird settings
bird_x = 80
bird_y = HEIGHT // 2
bird_vel = 0
gravity = 0.3
flap_strength = -8

# Pipe settings
pipe_width = 70
pipe_gap = 250
pipe_speed = 3

pipes = []
spawn_timer = 0

score = 0
dead = False
death_timer = 0


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

    if dead:
        death_timer += 1
        if death_timer > 90:  # show "AGNES BAD" for 1.5 seconds
            reset_game()
        WIN.fill((200, 50, 50))
        text = BIG_FONT.render("6    7", True, (255, 255, 255))
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2,
                        HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        continue

    # Bird physics
    bird_vel += gravity
    bird_y += bird_vel

    # Spawn pipes
    spawn_timer += 1
    if spawn_timer > 90:
        spawn_timer = 0
        pipes.append(spawn_pipe())

    # Move pipes and count score
    for p in pipes:
        p[0].x -= pipe_speed
        p[1].x -= pipe_speed

        # Award points when the pipe passes the bird
        if p[0].x + pipe_width == bird_x:
            score += 10

    # Remove off-screen pipes
    pipes = [p for p in pipes if p[0].x > -pipe_width]

    # Collision rectangles
    bird_rect = pygame.Rect(bird_x, bird_y, 25, 25)

    # Check ceiling/ground
    if bird_y <= 0 or bird_y >= HEIGHT - 25:
        dead = True

    # Pipe collision
    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            dead = True

    # ----------------- Draw -----------------
    WIN.fill((135, 206, 250))  # sky blue

    # Draw bird
    pygame.draw.rect(WIN, (255, 255, 0), bird_rect)

    # Draw pipes
    for top, bottom in pipes:
        pygame.draw.rect(WIN, (0, 255, 0), top)
        pygame.draw.rect(WIN, (0, 255, 0), bottom)

    # Draw score
    score_text = FONT.render(str(score), True, (0, 0, 0))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()
