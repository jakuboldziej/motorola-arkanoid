from classes import *

gridBlocks = pygame.sprite.Group()
gridBlocksAmount = 40
for i in range(gridBlocksAmount):
    if i < gridBlocksAmount/4:
        newGridBlock = GridBlock(i * WIDTH/10, HEIGHT/4-40, id=i+1)
    elif i < gridBlocksAmount/2:
        newGridBlock = GridBlock((i-10) * WIDTH/10, HEIGHT/4-10, id=i+1)
    elif i < gridBlocksAmount-10:
        newGridBlock = GridBlock((i-20) * WIDTH/10, HEIGHT/4+20, id=i+1)
    elif i < gridBlocksAmount:
        newGridBlock = GridBlock((i-30) * WIDTH/10, HEIGHT/4+50, id=i+1)

    gridBlocks.add(newGridBlock)

lista = [
    [{"1": "asdf"}{"2": "asdf"}{"3": "asdf"}{"4": "asdf"}{"5": "asdf"}],
    [],
    [],
    [],
    [],

]

choosingGridBlockHeight = HEIGHT/1.3 - 10
choosingGridBlocks = pygame.sprite.Group()
silverGridBlock = GridBlock(WIDTH/13, choosingGridBlockHeight, choosingGridBlock=True, color=SILVER[0])
orangeGridBlock = GridBlock(WIDTH/13 + 85, choosingGridBlockHeight, choosingGridBlock=True, color=ORANGE[0])
aquaGridBlock = GridBlock(WIDTH/13 + 85*2, choosingGridBlockHeight, choosingGridBlock=True, color=AQUA[0])
greenGridBlock = GridBlock(WIDTH/13 + 85*3, choosingGridBlockHeight, choosingGridBlock=True, color=GREEN[0])
redGridBlock = GridBlock(WIDTH/13 + 85*4, choosingGridBlockHeight, choosingGridBlock=True, color=RED[0])
blueGridBlock = GridBlock(WIDTH/13 + 85*5, choosingGridBlockHeight, choosingGridBlock=True, color=BLUE[0])
pinkGridBlock = GridBlock(WIDTH/13 + 85*6, choosingGridBlockHeight, choosingGridBlock=True, color=PINK[0])
goldGridBlock = GridBlock(WIDTH/13 + 85*7, choosingGridBlockHeight, choosingGridBlock=True, color=GOLD[0])

choosingGridBlocks.add(silverGridBlock)
choosingGridBlocks.add(orangeGridBlock)
choosingGridBlocks.add(aquaGridBlock)
choosingGridBlocks.add(greenGridBlock)
choosingGridBlocks.add(redGridBlock)
choosingGridBlocks.add(blueGridBlock)
choosingGridBlocks.add(pinkGridBlock)
choosingGridBlocks.add(goldGridBlock)