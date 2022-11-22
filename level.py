from classes import *

class Level:
    def __init__(self):
        super(Level, self).__init__()
        self.winscore = 0
        self.brickArray = []
        self.powerUpRate = 4
    
    def calcScore(self, brick):
        if brick.color in COLORFUL:
            self.winscore += brick.value

    def draw(self):
        with open("levels.json", "r+") as f:
            data = json.load(f)
            levels = data["levels"]

        if levels:
            for level in levels:
                levelId = level["levelId"]
                if int(levelId) == platform.currentLevel:
                    gridArray = level["gridArray"]
                    self.brickArray = gridArray

            startingY = 30*3
            startingX = 0
            brickCount = ROWCOUNT*15
                
            for i in range(brickCount):
                if i%15==0 and i != 0:
                    startingX -= WIDTH
                    startingY += 30

                brick = gridArray.get(f"{i+1}")
                if brick != None:
                    for color in COLORS:
                        if literal_eval(brick) == color[0]:
                            brickColor = color

                    newBrick = Brick(startingX+i*80, startingY, color=brickColor)
                    self.calcScore(newBrick)
                    bricks.add(newBrick)
        else:
            text1 = font.render('No Levels', True, (255, 255, 255))
            display.blit(text1, (WIDTH/2-text1.get_width()/2, HEIGHT/4-text1.get_height()/2))