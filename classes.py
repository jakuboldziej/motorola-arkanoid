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
        self.buttonText = buttonText

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.clicked = False
        self.alreadyPressed = False

        self.buttonSurf = font.render(self.buttonText, True, BLACK[0])
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def process(self):
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0] and self.clicked == False:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.clicked = True
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
                else:
                    self.alreadyPressed = False
            else:
                self.clicked = False
        
    def draw(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        display.blit(self.buttonSurface, self.buttonRect)

    def changeText(self, text):
        self.buttonText = text

        self.buttonSurf = font.render(self.buttonText, True, 'white')
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        display.blit(self.buttonSurface, self.buttonRect)

        print(self.buttonText)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.x = WIDTH/2
        self.y = HEIGHT-25
        self.surf = pygame.Surface((100, 25))
        self.surf.fill(WHITE[0])
        self.speed = 7
        self.rect = self.surf.get_rect(center=((self.x, self.y)))
        self.platformDirection = "center"
        self.currentPowerUp = None
        self.lifes = 3
        self.currentLevel = 1

    def update(self, pressed_keys):
        if settings.steeringType == "mouse":
            mousePos = pygame.mouse.get_pos()
            self.rect.x = mousePos[0] - self.rect.width/2
        else:
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
        pygame.draw.rect(display, WHITE[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))

    def releaseBall(self):
        if self.platformDirection == "left":
            ball.directionX = -ball.speedX
            ball.directionY = -ball.speedY
            ball.direction = "left," + ball.direction.split(",")[1]
        elif self.platformDirection == "right":
            ball.directionX = +ball.speedX
            ball.directionY = -ball.speedY
            ball.direction = "left," + ball.direction.split(",")[1]
        else:
            ball.directionX = 0
            ball.directionY = -ball.speedY
            ball.direction = "0," + ball.direction.split(",")[1]

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        # self.surf = pygame.Surface((11, 11))
        # self.surf.fill(WHITE[0])
        # self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 55))
        self.radius = 9
        self.rect = pygame.draw.circle(display, WHITE[0], (5, 5), 8)
        self.speed = 6
        self.speedX = self.speed
        self.speedY = self.speed
        self.directionX = 0 
        self.directionY = 0
        self.stick = True
        self.direction = "0,up"
    
    def draw(self):
        pygame.draw.circle(display, WHITE[0], (self.rect[0] + 7, self.rect[1] + 7), self.radius)
        # pygame.draw.rect(display, WHITE[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))

    def update(self):
        if ball.stick:
            self.direction = "right,up"
            self.directionX = 0
            self.directionY = 0
            ball.rect[0] = platform.rect[0] + platform.rect[2]/2 - ball.rect[2]/2
            ball.rect[1] = platform.rect[1] - 25
        else:
            if self.rect.bottom >= HEIGHT:
                ball.stick = True
                platform.lifes -= 1
            elif self.rect.top < 0:
                self.directionY = +self.speedY
                self.direction = self.direction.split(",")[0] + ",down"
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
        self.width = 80
        self.height = 30
        self.health = 1
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)

        if self.color in COLORFUL:
            if self.color == SILVER:
                self.value = color[1] * platform.currentLevel
                self.health = 2
                for i in range(platform.currentLevel+1):
                    if i % 8 == 0 and i != 0:
                        self.health += 1
            else:
                self.health = 1
                self.value = color[1]
        else:
            self.health = -1

    def draw(self):
        pygame.draw.rect(display, self.color[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
        pygame.draw.rect(display, WHITE[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 1)

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

class GridBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, choosingGridBlock=False, editingGridBlock=False,  color=WHITE, id=0):
        super(GridBlock, self).__init__()
        self.id = id
        self.x = x
        self.y = y
        self.choosingGridBlock = choosingGridBlock
        self.editingGridBlock = editingGridBlock
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
                pygame.draw.rect(display, self.color[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 1)
            else:
                pygame.draw.rect(display, self.color[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
                pygame.draw.rect(display, WHITE[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]), 1)
        else:
            pygame.draw.rect(display, self.color[0], pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]))
            
    def process(self):
        mousePos = pygame.mouse.get_pos()
        gridBlockCollision = self.rect.collidepoint(mousePos)
        if gridBlockCollision:
            if not self.choosingGridBlock:
                self.surf.fill(mouse.choosingColor[0])
            else:
                self.surf.fill(self.color[0])
            
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.clicked:
                    self.clicked = True
                    if not self.choosingGridBlock:
                        if not self.selected:
                            # Creating brick on gridBlock
                            self.color = mouse.choosingColor
                            self.selected = True
                            self.manageArray(append=True)
                        else:
                            self.color = WHITE
                            self.selected = False
                            self.manageArray(append=False)
                    else:
                        if not self.selected:
                            mouse.choosingColor = self.color
                            self.selected = True
                        else:
                            self.selected = False
            else:
                self.clicked = False
            display.blit(self.surf, self.rect)

    def manageArray(self, append):
        if append:
            editorClass.editingGridBlockArray[f"{self.id}"] =  str(self.color[0])
        else:
            editorClass.editingGridBlockArray.pop(f"{self.id}")

class Editor(pygame.sprite.Sprite):
    def __init__(self):
        super(Editor, self).__init__()
        self.editingGridBlockArray = dict()
        self.currentLevel = 1
        self.editing = True
        self.resetArray()
        print(self.currentLevel)
    
    def resetArray(self):
        self.editingGridBlockArray = dict()
        self.choosingColor = SILVER

    def creatingGrid(self):
        self.resetArray()
        for gridBlock in gridBlocks:
            gridBlock.kill()
        with open("levels.json", "r+") as f:
            data = json.load(f)
            levels = data["levels"]
        
        if not levels:
            self.currentLevel = 1
            
            brickCount = ROWCOUNT*15
            startingY = 30*3
            startingX = 0
            for i in range(brickCount):
                if i%15==0 and i != 0:
                    startingX -= WIDTH
                    startingY += 30

                # print(i*80, startingX, startingY)
                newGridBlock = GridBlock(startingX+i*80, startingY, id=i+1)
                gridBlocks.add(newGridBlock)
        else:
            if self.editing:
                for level in levels:
                    levelId = level["levelId"]
                    if int(levelId) == self.currentLevel:
                        gridArray = level["gridArray"]
                        self.brickArray = gridArray
                
                editorClass.editingGridBlockArray = dict(gridArray)

                brickCount = ROWCOUNT*15
                startingY = 30*3
                startingX = 0
                for i in range(brickCount):
                    if i%15==0 and i != 0:
                        startingX -= WIDTH
                        startingY += 30

                    gridBlock = gridArray.get(f"{i+1}")
                    if gridBlock != None:
                        for color in COLORS:
                            if literal_eval(gridBlock) == color[0]:
                                gridBlockColor = color

                        newGridBlock = GridBlock(startingX+i*80, startingY, id=i+1, editingGridBlock=True, color=gridBlockColor)
                        newGridBlock.selected = True
                    else:
                        newGridBlock = GridBlock(startingX+i*80, startingY, id=i+1, editingGridBlock=True)
                    gridBlocks.add(newGridBlock)
            else:
                brickCount = ROWCOUNT*15
                startingY = 30*3
                startingX = 0
                for i in range(brickCount):
                    if i%15==0 and i != 0:
                        startingX -= WIDTH
                        startingY += 30

                    # print(i*80, startingX, startingY)
                    newGridBlock = GridBlock(startingX+i*80, startingY, id=i+1)
                    gridBlocks.add(newGridBlock)
                
        # print(editorClass.editingGridBlockArray)

        choosingGridBlockHeight = HEIGHT/1.3 - 10
        silverGridBlock = GridBlock(WIDTH/2 - 85*4, choosingGridBlockHeight, choosingGridBlock=True, color=SILVER)
        orangeGridBlock = GridBlock(WIDTH/2 - 85*3, choosingGridBlockHeight, choosingGridBlock=True, color=ORANGE)
        aquaGridBlock = GridBlock(WIDTH/2 - 85*2, choosingGridBlockHeight, choosingGridBlock=True, color=AQUA)
        greenGridBlock = GridBlock(WIDTH/2 - 85, choosingGridBlockHeight, choosingGridBlock=True, color=GREEN)
        redGridBlock = GridBlock(WIDTH/2, choosingGridBlockHeight, choosingGridBlock=True, color=RED)
        blueGridBlock = GridBlock(WIDTH/2 + 85, choosingGridBlockHeight, choosingGridBlock=True, color=BLUE)
        pinkGridBlock = GridBlock(WIDTH/2 + 85*2, choosingGridBlockHeight, choosingGridBlock=True, color=PINK)
        goldGridBlock = GridBlock(WIDTH/2 + 85*3, choosingGridBlockHeight, choosingGridBlock=True, color=GOLD)

        choosingGridBlocks.add(silverGridBlock)
        choosingGridBlocks.add(orangeGridBlock)
        choosingGridBlocks.add(aquaGridBlock)
        choosingGridBlocks.add(greenGridBlock)
        choosingGridBlocks.add(redGridBlock)
        choosingGridBlocks.add(blueGridBlock)
        choosingGridBlocks.add(pinkGridBlock)
        choosingGridBlocks.add(goldGridBlock)

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        self.pos = pygame.mouse.get_pos()
        self.surf = pygame.Surface((0.1, 0.1))
        self.surf.fill(WHITE[0])
        self.rect = self.surf.get_rect(center=(self.pos[0], self.pos[1]))
        self.choosingColor = SILVER

class Settings:
    def __init__(self):
        super(Settings, self).__init__()
        self.steeringType = "keyboard"

settings = Settings()

editorClass = Editor()
platform = Platform()
ball = Ball()
mouse = Mouse()


bricks = pygame.sprite.Group()
# balls = pygame.sprite.Group()
powerUps = pygame.sprite.Group()
gridBlocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
choosingGridBlocks = pygame.sprite.Group()
# all_sprites.add(ball)