from classes import *

import random

class Level:
    def __init__(self, brickAmount):
        super(Level, self).__init__()
        self.brickAmount = brickAmount
        self.winscore = 0
        self.Spacebetween = 90   # odstep miedzy blokami
        self.Margin = 85 #poczatkowy margines

    def draw(self):
        Testbrick = Brick(0,0,random.choice(COLORS))
        brickx = Testbrick.get_width()
        self.Margin = (WIDTH+self.brickAmount/2 - (brickx *self.brickAmount/2))/2    #self.brickAmount/ilość kolumn
        for i in range(self.brickAmount):
            if i < self.brickAmount/2:
                new_brick = Brick(self.Margin + i*self.Spacebetween, HEIGHT/4, random.choice(COLORS))
                if new_brick.color in COLORFUL: 
                    self.winscore += new_brick.color[1]
                elif new_brick.color == SILVER:
                    self.winscore += new_brick.color[1] * CURRENTLEVEL
            else:
                new_brick = Brick(self.Margin + (i-8)*self.Spacebetween, HEIGHT/4 - 40, random.choice(COLORS))
                if new_brick.color in COLORFUL: 
                    self.winscore += new_brick.color[1]
                elif new_brick.color == SILVER:
                    self.winscore += new_brick.color[1] * CURRENTLEVEL

            bricks.add(new_brick)
            all_sprites.add(new_brick)

