import random
import pygame

# Game Sizes
BLOCK_SIZE = 32
M = 1  # Margin
ROW = 22 - M*2
COL = 12 - M*2
WIDTH = COL*BLOCK_SIZE + 2*M*BLOCK_SIZE
HEIGHT = ROW*BLOCK_SIZE + 2*M*BLOCK_SIZE

# Colors
BG = (0, 27, 46)  # Background Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 215, 0)
PURPLE = (127, 0, 255)
YELLOW = (254, 198, 1)
PINK = (255, 105, 180)

# Shapes
car = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
    [1, 0, 1]
]


pygame.init()
pygame.display.set_caption("Brick Car")
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class Object:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = WHITE


def get_player():
    return Object(2, -4, car)


enemy_xpos = [2, 5]


def get_enemy():
    return Object(random.choice(enemy_xpos), 0, car)


player = get_player()
enemy = get_enemy()


def get_object_pos(object):
    positions = []
    for y, row in enumerate(object.shape):
        for x, col in enumerate(row):
            if col == 1:
                positions.append((object.y + y, object.x + x))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])
    return positions


def draw_guide(surface, row, col):
    for x in range(col):
        pygame.draw.line(surface, GRAY, (BLOCK_SIZE*M + x*BLOCK_SIZE, BLOCK_SIZE*M),
                         (BLOCK_SIZE*M + x*BLOCK_SIZE, HEIGHT - BLOCK_SIZE*M))
        for y in range(row):
            pygame.draw.line(surface, GRAY, (BLOCK_SIZE*M, BLOCK_SIZE*M + y*BLOCK_SIZE),
                             (WIDTH - BLOCK_SIZE*M, BLOCK_SIZE*M + y*BLOCK_SIZE))


def draw_window(surface):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (BLOCK_SIZE*M + x*BLOCK_SIZE,
                             BLOCK_SIZE*M + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


###############################################################################
done = False

tick = pygame.USEREVENT
tick_speed = 300
pygame.time.set_timer(tick, tick_speed)

spawn = pygame.USEREVENT+1
spawn_time = tick_speed*4
pygame.time.set_timer(spawn, spawn_time)

while not done:
    grid = [[BG for _ in range(COL)] for _ in range(ROW)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == tick:
            enemy.y += 1
        if event.type == spawn:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x = 2
            if event.key == pygame.K_RIGHT:
                player.x = 5

    player_pos = get_object_pos(player)
    for i in range(len(player_pos)):
        y, x = player_pos[i]
        grid[y][x] = player.color

    enemy_pos = get_object_pos(enemy)
    for i in range(len(enemy_pos)):
        y, x = enemy_pos[i]
        if y < ROW:
            grid[y][x] = enemy.color

    draw_window(SCREEN)
    draw_guide(SCREEN, ROW + 1, COL + 1)

    pygame.display.flip()  # Draw the screen each frame
###############################################################################
