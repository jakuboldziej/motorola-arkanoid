import pygame
from config import *

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((100, 25))
        self.surf.fill(WHITE)
        self.x = WIDTH/2
        self.y = HEIGHT-25
        self.rect = self.surf.get_rect(center=((self.x, self.y)))
        self.platformDirection = "center"

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
            # self.rect[0] -= 5
            self.platformDirection = "left"
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)
            # self.rect[0] += 5
            self.platformDirection = "right"
        else:
            self.platformDirection = "center"
        if ball.stick == True:
            if pressed_keys[K_SPACE]:
                ball.stick = False
                if self.platformDirection == "left":
                    ball.directionX = -ball.speedX
                    ball.directionY = -ball.speedY
                    ball.direction = "left," + ball.direction.split(",")[1]
                elif self.platformDirection == "right":
                    ball.directionX = +ball.speedX
                    ball.directionY = -ball.speedY
                    ball.direction = "right," + ball.direction.split(",")[1]
                else:
                    ball.directionX = 0
                    ball.directionY = -ball.speedY
                    ball.direction = "0," + ball.direction.split(",")[1]

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        # self.surf = pygame.Surface((11, 11))
        # self.surf.fill(WHITE)
        # self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 55))
        self.radius = 9
        self.rect = pygame.draw.circle(display, WHITE, (5, 5), 8)
        self.speedX = 4
        self.speedY = 4
        self.directionX = 0 
        self.directionY = 0
        self.stick = True
        self.direction = "0,up"
    
    def draw(self):
        pygame.draw.circle(display, WHITE, (self.rect[0] + 7, self.rect[1] + 7), self.radius)
        # pygame.draw.rect(display, WHITE, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))

    def update(self):
        if ball.stick:
            self.direction = "right,up"
            self.directionX = 0
            self.directionY = 0
            ball.rect[0] = platform.rect[0] + 45
            ball.rect[1] = platform.rect[1] - 25
        else:
            if self.rect.bottom >= WIDTH - 180:
                ball.stick = True
            elif self.rect.top < 0:
                self.directionY = +self.speedY
                self.direction = self.direction.split(",")[0] +",down"
            elif self.rect.left < 0:
                self.directionX = +self.speedX
                self.direction = "right," + self.direction.split(",")[1]
            elif self.rect.right > WIDTH:
                self.directionX = -self.speedX
                self.direction = "left," + self.direction.split(",")[1]
                
            self.rect.move_ip(self.directionX, self.directionY)

    def collision(self):
        global SCORE
        if pygame.sprite.collide_rect(platform, ball):
            self.direction = self.direction.split(",")[0] + ",up"
            center = platform.rect[2]//3
            collidePoint = ball.rect[0] + ball.rect[2] - platform.rect[0]
            # XD
            if center < collidePoint < center*2:
                if platform.platformDirection == "left":
                    self.directionX = -5
                elif platform.platformDirection == "right":
                    self.directionX = 5
                print("center")
            elif collidePoint > center*2:
                if platform.platformDirection == "left":
                    self.directionX = -3
                elif platform.platformDirection == "right":
                    self.directionX = 3
                print("right")
            else:
                if platform.platformDirection == "left":
                    self.directionX = -3
                elif platform.platformDirection == "right":
                    self.directionX = 3
                print("left")
                
            self.directionY = -self.speedY
            self.rect.move_ip(self.directionX, self.directionY)

        collision = pygame.sprite.spritecollide(ball, bricks, False)
        for brick in collision:
            if self.rect.left < brick.rect.right and self.direction.split(",")[0] == "left" and not self.rect.right < brick.rect.right:
                self.directionX = +self.speedX
                # print(self.direction.split(","), "RIGHT")
            elif self.rect.right > brick.rect.left and self.direction.split(",")[0] == "right" and not self.rect.left > brick.rect.left:
                self.directionX = -self.speedX
                # print(self.direction.split(","), "LEFT")
            elif self.rect.top < brick.rect.bottom and self.rect.bottom > brick.rect.bottom:
                self.directionY = +self.speedY
                # print(self.direction.split(","), "BOTTOM")
            elif self.rect.bottom > brick.rect.top and self.direction.split(",")[1] == "down":
                self.directionY = -self.speedY
                # print(self.direction.split(","), "TOP")
            brick.kill()
            # Score logic
            SCORE += 10

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

platform = Platform()
ball = Ball()
bricks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(platform)
# all_sprites.add(ball)