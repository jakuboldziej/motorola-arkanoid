from classes import *

import random

class Level:
    def __init__(self, brickAmount):
        super(Level, self).__init__()
        self.brickAmount = brickAmount
        self.winscore = 0
    
    def draw(self):
        for i in range(self.brickAmount):
            if i < self.brickAmount/2:
                new_brick = Brick(85 + i*90, HEIGHT/4, random.choice(COLORS))
                if new_brick.color in COLORFUL: 
                    self.winscore += new_brick.color[1]
                elif new_brick.color == SILVER:
                    self.winscore += new_brick.color[1] * CURRENTLEVEL
            else:
                new_brick = Brick(85 + (i-8)*90, HEIGHT/4 - 40, random.choice(COLORS))
                if new_brick.color in COLORFUL: 
                    self.winscore += new_brick.color[1]
                elif new_brick.color == SILVER:
                    self.winscore += new_brick.color[1] * CURRENTLEVEL

            bricks.add(new_brick)
            all_sprites.add(new_brick)