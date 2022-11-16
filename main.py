import pygame
from pygame.locals import *

import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((100, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=((WIDTH/2, HEIGHT-25)))
        self.playerDirection = "center"

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
            self.playerDirection = "left"
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
            self.playerDirection = "right"
        else:
            self.playerDirection = "center"

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(WIDTH/2, 0))
        self.speedX = 0
        self.speedY = 1
        self.directionX = self.speedX  
        self.directionY = self.speedY
        
    def update(self):
        self.rect.move_ip(self.directionX, self.directionY)
        if self.rect.bottom >= WIDTH:
            self.directionY = -self.speedY
            # self.kill()
        elif self.rect.top < 0:
            self.directionY = self.speedY
        elif self.rect.left < 0:
            self.directionX = 1
        elif self.rect.right > WIDTH:
            self.directionX = -1

    def collision(self):
        if pygame.sprite.collide_rect(player, ball):
            if player.playerDirection == "left":
                self.speedX = -1
                self.directionX = self.speedX
            elif player.playerDirection == "right":
                self.speedX = 1
                self.directionX = self.speedX
            self.directionY = -self.speedY
            self.rect.move_ip(self.directionX, self.directionY)

pygame.init()

WIDTH, HEIGHT = 800, 600

display = pygame.display.set_mode((WIDTH, HEIGHT))

player = Player()
ball = Ball()

background = pygame.Surface(display.get_size())
background.fill((0, 0, 0))

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)

def drawWindow():
    display.blit(background, (0, 0))
    
    display.blit(player.surf, player.rect)

    display.blit(ball.surf, ball.rect)

    pygame.display.flip()

def updateEntites():
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    ball.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    drawWindow()
    updateEntites()
    ball.collision()