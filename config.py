from pygame import time
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)

WIDTH, HEIGHT = 800, 600
FPS = 60
SCORE = 0
clock = time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)