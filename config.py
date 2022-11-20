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

BASEDIR = path.dirname(path.realpath(__file__))

ROWCOUNT = 5
SCORE = 0
PREVSCORE = 0
FPS = 60
clock = pygame.time.Clock()
playing = False

# Colors
BLACK = ((0, 0, 0), 0)
WHITE = ((255, 255, 255), 0)
SILVER = ((209, 208, 207), 50)
ORANGE = ((199, 88, 2), 60)
AQUA = ((87, 228, 250), 70)
GREEN = ((5, 255, 80), 80)
RED = ((255, 0, 0), 90)
BLUE = ((4, 24, 204), 100)
PINK = ((226, 5, 255), 110)
GOLD = ((251, 255, 5), 120)

COLORS = (SILVER, ORANGE, AQUA, GREEN, RED, BLUE, PINK, GOLD)

COLORFUL = (SILVER, ORANGE, AQUA, GREEN, RED, BLUE, PINK)

WIDTH, HEIGHT = 800, 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')

background = pygame.Surface(display.get_size())
background.fill(BLACK[0])