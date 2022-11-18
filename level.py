from classes import *

def level1():
    for i in range(8):
        new_brick = Brick(80 + i*90, HEIGHT/4)
        bricks.add(new_brick)
        all_sprites.add(new_brick)

    for i in range(8):
        new_brick = Brick(80 + i*90, HEIGHT/4 - 40)
        bricks.add(new_brick)
        all_sprites.add(new_brick)