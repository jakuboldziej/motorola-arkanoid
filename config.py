from pygame import time, display, Surface
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
display = display.set_mode((WIDTH, HEIGHT))

background = Surface(display.get_size())
background.fill(BLACK)

FPS = 60
SCORE = 0
clock = time.Clock()