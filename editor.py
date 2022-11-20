from classes import *

gridBlocks = pygame.sprite.Group()
brickCount = ROWCOUNT*10
startingY = 30*3
startingX = 0
for i in range(brickCount):
    if i%10==0 and i != 0:
        startingX -= WIDTH
        startingY += 30

    # print(i*80, startingX, startingY)
    newGridBlock = GridBlock(startingX+i*80, startingY, id=i+1)
    gridBlocks.add(newGridBlock)

choosingGridBlockHeight = HEIGHT/1.3 - 10
choosingGridBlocks = pygame.sprite.Group()
silverGridBlock = GridBlock(WIDTH/13, choosingGridBlockHeight, choosingGridBlock=True, color=SILVER)
orangeGridBlock = GridBlock(WIDTH/13 + 85, choosingGridBlockHeight, choosingGridBlock=True, color=ORANGE)
aquaGridBlock = GridBlock(WIDTH/13 + 85*2, choosingGridBlockHeight, choosingGridBlock=True, color=AQUA)
greenGridBlock = GridBlock(WIDTH/13 + 85*3, choosingGridBlockHeight, choosingGridBlock=True, color=GREEN)
redGridBlock = GridBlock(WIDTH/13 + 85*4, choosingGridBlockHeight, choosingGridBlock=True, color=RED)
blueGridBlock = GridBlock(WIDTH/13 + 85*5, choosingGridBlockHeight, choosingGridBlock=True, color=BLUE)
pinkGridBlock = GridBlock(WIDTH/13 + 85*6, choosingGridBlockHeight, choosingGridBlock=True, color=PINK)
goldGridBlock = GridBlock(WIDTH/13 + 85*7, choosingGridBlockHeight, choosingGridBlock=True, color=GOLD)

choosingGridBlocks.add(silverGridBlock)
choosingGridBlocks.add(orangeGridBlock)
choosingGridBlocks.add(aquaGridBlock)
choosingGridBlocks.add(greenGridBlock)
choosingGridBlocks.add(redGridBlock)
choosingGridBlocks.add(blueGridBlock)
choosingGridBlocks.add(pinkGridBlock)
choosingGridBlocks.add(goldGridBlock)