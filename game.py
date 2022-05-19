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
    return Object(2, ROW-4, car)


def get_enemy():
    return Object(random.choice([2, 5]), -4, car)


player = get_player()
all_enemies = []


def get_object_pos(object, enemy=False):
    positions = []
    for y, row in enumerate(object.shape):
        for x, col in enumerate(row):
            if col == 1:
                positions.append((object.y + y, object.x + x))
    for i, pos in enumerate(positions):
        positions[i] = [pos[0], pos[1]]
    if enemy:
        all_enemies.extend(positions)
    else:
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

    # Score text
    font = pygame.font.SysFont("Calibri", 20)
    text = font.render("Score: ", True, WHITE)

    SCREEN.blit(text, (8, 8))


###############################################################################
done = False
gameover = False

tick = pygame.USEREVENT
tick_speed = 150
pygame.time.set_timer(tick, tick_speed)

spawn = pygame.USEREVENT+1
spawn_time = tick_speed*9
pygame.time.set_timer(spawn, spawn_time)

move_enemies = False
INF = 999999999

score = 0
temp_score = 0
while not done:
    SCREEN.fill(BLACK)
    grid = [[BG for _ in range(COL)] for _ in range(ROW)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == tick:
            if move_enemies:
                for i in all_enemies:
                    i[0] += 1
        if event.type == spawn:
            get_object_pos(get_enemy(), True)
            move_enemies = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x = 2
            if event.key == pygame.K_RIGHT:
                player.x = 5

    player_pos = get_object_pos(player)
    for i in range(len(player_pos)):
        y, x = player_pos[i]
        grid[y][x] = player.color

    if move_enemies:
        for i in all_enemies:
            y, x = i
            if y >= ROW:
                all_enemies.remove(i)
                temp_score += 100/7
            if 0 <= y < ROW:
                grid[y][x] = WHITE

    if not(round(temp_score) % 100):
        score += round(temp_score)
        temp_score = 0

    draw_window(SCREEN)

    font = pygame.font.SysFont("Calibri", 20)
    text = font.render(str(round(score)), True, WHITE)
    SCREEN.blit(text, (BLOCK_SIZE*2, 8))

    draw_guide(SCREEN, ROW + 1, COL + 1)

    ############ GAME OVER ############
    player_under = [player.y+3, player.x+1]
    temp_pos = player_pos
    if player_under not in temp_pos:
        temp_pos.append(player_under)
    for block in all_enemies:
        if block in temp_pos:
            tick_speed = INF
            spawn_time = tick_speed
            pygame.time.set_timer(tick, tick_speed)
            pygame.time.set_timer(spawn, spawn_time)
            gameover = True
    ###################################

    pygame.display.flip()  # Draw the screen each frame
###############################################################################
