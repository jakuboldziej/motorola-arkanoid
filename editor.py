from classes import *

gridBlocks = pygame.sprite.Group()
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

choosingGridBlockHeight = HEIGHT/1.3 - 10
choosingGridBlocks = pygame.sprite.Group()
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