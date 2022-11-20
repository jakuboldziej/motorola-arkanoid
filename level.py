from classes import *

from ast import literal_eval

class Level:
    def __init__(self):
        super(Level, self).__init__()
        self.winscore = 0
        self.brickArray = []
    
    def calcScore(self, brick):
        if brick.color in COLORFUL:
            self.winscore += brick.value

    def draw(self):
        with open("levels.json", "r+") as f:
            data = json.load(f)
            levels = data["levels"]
        for level in levels:
            levelId = level["levelId"]
            if int(levelId) == platform.currentLevel:
                gridArray = level["gridArray"]
                self.brickArray = gridArray
        

        startingY = 30*3
        startingX = 0
        brickCount = ROWCOUNT*10
        for i, brick in enumerate(gridArray):
            if i%10==0 and i != 0:
                    startingX -= WIDTH
                    startingY += 30

            if brick[f"{i+1}"] == 1:
                for color in COLORS:
                    if literal_eval(brick["color"]) == color[0]:
                        brickColor = color

                newBrick = Brick(startingX+i*80, startingY, color=brickColor)
                self.calcScore(newBrick)
                bricks.add(newBrick)