from classes import *

class Level:
    def __init__(self):
        super(Level, self).__init__()
        self.winscore = 0
        self.brickArray = []
    
    def calcScore(self, brick):
        if brick.color in COLORFUL: 
            if brick.color == SILVER:
                self.winscore += brick.color[1] * CURRENTLEVEL
            else:
                self.winscore += brick.color[1]

    def draw(self):
        for i in range(32):
            if i < 32/4:
                new_brick = Brick(i * WIDTH/10+120, HEIGHT/4-40, color=random.choice(COLORS))
                self.calcScore(new_brick)
            # elif i < 32/4+8:
            #     new_brick = Brick((i-7) * WIDTH/10+40, HEIGHT/4-10, color=random.choice(COLORS))
            #     self.calcScore(new_brick)
            # elif i < 32/4+16:
            #     new_brick = Brick((i-15) * WIDTH/10+40, HEIGHT/4+20, color=random.choice(COLORS))
            #     self.calcScore(new_brick)
            # elif i < 32/4+24:
            #     new_brick = Brick((i-23) * WIDTH/10+40, HEIGHT/4+50, color=random.choice(COLORS))
            #     self.calcScore(new_brick)

            bricks.add(new_brick)