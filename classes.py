from config import *

pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=True):
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
        self.x = WIDTH/2
        self.y = HEIGHT-25
        self.surf = pygame.Surface((100, 25))
        self.surf.fill(WHITE)
        self.speed = 7
        self.rect = self.surf.get_rect(center=((self.x, self.y)))
        self.platformDirection = "center"
        self.currentPowerUp = None
        self.lifes = 3

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
        if ball.stick == True and ball.rect[1] < WIDTH - 200:
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

    def draw(self):
        pygame.draw.rect(display, WHITE, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        # self.surf = pygame.Surface((11, 11))
        # self.surf.fill(WHITE)
        # self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 55))
        self.radius = 9
        self.rect = pygame.draw.circle(display, WHITE, (5, 5), 8)
        self.speed = 6
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
            ball.rect[0] = platform.rect[0] + platform.rect[2]/2 - ball.rect[2]/2
            ball.rect[1] = platform.rect[1] - 25
        else:
            if self.rect.bottom >= WIDTH - 180:
                ball.stick = True
                platform.lifes -= 1
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

    def draw(self):
        pygame.draw.rect(display, self.color[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
        pygame.draw.rect(display, WHITE, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 1)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super(PowerUp, self).__init__()
        self.x = x
        self.y = y
        self.color = color
        self.typeList = ["longerPlatform", "moreBalls", "strongerHit", "extraLife", "laser", "catchingMode"]
        self.speed = 3
        self.surf = pygame.Surface((80, 80))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        self.rect[1] += self.speed
    
    def restartBoosts(self):
        platform.rect[2] = 100

    def boost(self):
        self.restartBoosts()
        boostType = random.choice(self.typeList)
        if boostType == "longerPlatform":
            platform.rect[2] = 150
            platform.currentPowerUp = "longerPlatform"
        elif boostType == "moreBalls":
            platform.currentPowerUp = "moreBalls"
        elif boostType == "strongerHit":
            platform.currentPowerUp = "strongerHit"
        elif boostType == "extraLife":
            platform.lifes += 1
            platform.currentPowerUp = "extraLife"
        elif boostType == "laser":
            platform.currentPowerUp = "laser"
        elif boostType == "catchingMode":
            platform.currentPowerUp = "catchingMode"
        print(boostType)

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        self.pos = pygame.mouse.get_pos()
        self.surf = pygame.Surface((0.1, 0.1))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(self.pos[0], self.pos[1]))
        self.choosingColor = SILVER[0]

class Editor:
    def __init__(self):
        super(Editor, self).__init__()
        self.width = WIDTH
        self.height = HEIGHT - 400
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(WIDTH/2, 0))

editingGridBlockArray = []
class GridBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, choosingGridBlock=False, color=WHITE, id=0):
        super(GridBlock, self).__init__()
        self.id = id
        self.x = x
        self.y = y
        self.choosingGridBlock = choosingGridBlock
        self.width = 80
        self.height = 30
        self.color = color
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.clicked = False
        self.selected = False

    def draw(self):
        if not self.choosingGridBlock:
            if not self.selected:
                pygame.draw.rect(display, self.color, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 1)
            else:
                pygame.draw.rect(display, self.color, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
                pygame.draw.rect(display, WHITE, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 1)
        else:
            pygame.draw.rect(display, self.color, pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
            
    def process(self):
        mousePos = pygame.mouse.get_pos()
        gridBlockCollision = self.rect.collidepoint(mousePos[0], mousePos[1])
        if gridBlockCollision:
            if not self.choosingGridBlock:
                self.surf.fill(mouse.choosingColor)
            else:
                self.surf.fill(self.color)
            
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.clicked:
                    self.clicked = True
                    if not self.choosingGridBlock:
                        if not self.selected:
                            self.color = mouse.choosingColor
                            self.selected = True
                            editingGridBlockArray.append(self)
                        else:
                            self.color = WHITE
                            self.selected = False
                            editingGridBlockArray.remove(self)
                        print(self.id)
                    else:
                        if not self.selected:
                            mouse.choosingColor = self.color
                            self.selected = True
                        else:
                            self.selected = False
            else:
                self.clicked = False
            display.blit(self.surf, self.rect)

platform = Platform()
ball = Ball()
mouse = Mouse()

bricks = pygame.sprite.Group()
# balls = pygame.sprite.Group()
powerUps = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# all_sprites.add(ball)

