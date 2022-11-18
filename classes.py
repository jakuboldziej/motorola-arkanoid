from config import *

pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self):
        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        display.blit(self.buttonSurface, self.buttonRect)

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((100, 25))
        self.surf.fill(WHITE)
        self.speed = 7
        self.x = WIDTH/2
        self.y = HEIGHT-25
        self.rect = self.surf.get_rect(center=((self.x, self.y)))
        self.platformDirection = "center"

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            # self.rect[0] -= 5
            self.platformDirection = "left"
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(+self.speed, 0)
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
        self.speed = 8
        self.speedX = self.speed
        self.speedY = self.speed
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

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super(Brick, self).__init__()
        self.x = x
        self.y = y
        self.color = color
        self.health = 1
        self.value = color[1]
        self.surf = pygame.Surface((80, 30))
        self.surf.fill(color[0])
        self.rect = self.surf.get_rect(center=(x, y))

        if self.color in COLORFUL:
            self.health = 1
            if self.color == SILVER:
                self.health = 2
                for i in range(CURRENTLEVEL+1):
                    if i % 8 == 0 and i != 0:
                        self.health += 1
        else:
            self.health = -1


platform = Platform()
ball = Ball()

bricks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# all_sprites.add(ball)