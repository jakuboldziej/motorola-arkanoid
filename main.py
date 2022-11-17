import pygame
from config import *

import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((100, 25))
        self.surf.fill(WHITE)
        self.x = WIDTH/2
        self.y = HEIGHT-25
        self.rect = self.surf.get_rect(center=((self.x, self.y)))
        self.playerDirection = "center"

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            # self.rect[0] -= 5
            self.playerDirection = "left"
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            # self.rect[0] += 5
            self.playerDirection = "right"
        else:
            self.playerDirection = "center"
        if ball.stick == True:
            if pressed_keys[K_SPACE]:
                ball.stick = False
                if self.playerDirection == "left":
                    ball.directionX = -5
                    ball.directionY = -5
                elif self.playerDirection == "right":
                    ball.directionX = 5
                    ball.directionY = -5
                else:
                    ball.directionX = 0
                    ball.directionY = -5

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 55))
        self.directionX = 0 
        self.directionY = 0
        self.stick = True
        self.direction = "up"
        
    def update(self):
        if ball.stick:
            self.direction = "up"
            self.directionX = 0
            self.directionY = 0
            ball.rect[0] = player.rect[0] + 45
            ball.rect[1] = player.rect[1] - 25
        else:
            if self.rect.bottom >= WIDTH - 180:
                ball.stick = True
            elif self.rect.top < 0:
                self.directionY = 5
                self.direction = "down"
            elif self.rect.left < 0:
                self.directionX = 5
                self.direction = "right"
            elif self.rect.right > WIDTH:
                self.directionX = -5
                self.direction = "left"
                
            self.rect.move_ip(self.directionX, self.directionY)

    def collision(self):
        if pygame.sprite.collide_rect(player, ball):
            if player.playerDirection == "left":
                self.directionX = -random.randint(1, 5)
            elif player.playerDirection == "right":
                self.directionX = random.randint(1, 5)
            self.directionY = -5
            self.rect.move_ip(self.directionX, self.directionY)

        # hit_list = pygame.sprite.spritecollide(self, bricks, False)
        # for brick in hit_list:
        #     if self.rect[0] + self.rect[2] > brick.rect[0]:
        #         print("right")

        collision = pygame.sprite.spritecollideany(ball, bricks)
        if collision:
            if self.direction == "left":
                self.directionX = 5
            elif self.direction == "right":
                self.directionX = -5
            elif self.direction == "down":
                self.directionY = -5
            else:
                self.directionY = 5
            collision.kill()


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Brick, self).__init__()
        self.surf = pygame.Surface((80, 30))
        self.surf.fill((255, 0, 0))
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.Surface(display.get_size())
background.fill(BLACK)

player = Player()
ball = Ball()

bricks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)

for i in range(8):
    new_brick = Brick(80 + i*90, HEIGHT/4)
    bricks.add(new_brick)
    all_sprites.add(new_brick)

for i in range(8):
    new_brick = Brick(80 + i*90, HEIGHT/4 - 40)
    bricks.add(new_brick)
    all_sprites.add(new_brick)

def drawWindow():
    display.blit(background, (0, 0))
    for entity in all_sprites:
        display.blit(entity.surf, entity.rect)

    pygame.display.flip()

def updateEntites():
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    ball.update()

def debugging():
    # print("PLAYER", player.rect[0], player.rect[1])
    # print("BALL", ball.directionX, ball.directionY)
    # print(ball.rect[0], ball.rect[1])
    pass

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

    debugging()

    clock.tick(FPS)