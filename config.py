import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)
from os import path
import random
import json
from ast import literal_eval

BASEDIR = path.dirname(path.realpath(__file__))

ROWCOUNT = 15
SCORE = 0
PREVSCORE = 0
FPS = 60
clock = pygame.time.Clock()
playing = False

# Colors
BLACK = ((0, 0, 0), 0)
WHITE = ((255, 255, 255), 50)
ORANGE = ((199, 88, 2), 60)
AQUA = ((87, 228, 250), 70)
GREEN = ((5, 255, 80), 80)
RED = ((255, 0, 0), 90)
BLUE = ((4, 24, 204), 100)
PINK = ((226, 5, 255), 110)
YELLOW = ((251, 255, 5), 120)
SILVER = ((209, 208, 207), 50)
GOLD = ((168, 125, 7), 0)

COLORS = (SILVER, GOLD, ORANGE, AQUA, GREEN, RED, BLUE, PINK, YELLOW, WHITE)

COLORFUL = (WHITE, SILVER, ORANGE, AQUA, GREEN, RED, BLUE, PINK, YELLOW)

WIDTH, HEIGHT = 1200, 800
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

background = pygame.Surface(display.get_size())
background.fill(BLACK[0])