import pygame
from config import *
from classes import *
from level import *

pygame.init()

# Level management
def loadlevels():
    level1()

# Drawing and updating
def drawScore():
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    text = font.render('Score: ' + str(SCORE), True, (0, 255, 0))
    display.blit(text, (10, 10))

def drawWindow():
    display.blit(background, (0, 0))
    for entity in all_sprites:
        display.blit(entity.surf, entity.rect)

    ball.draw()

    drawScore()

    pygame.display.flip()

def updateEntites():
    pressed_keys = pygame.key.get_pressed()

    platform.update(pressed_keys)
    ball.update()

# Loops
def winScreen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        fontt = pygame.font.Font(pygame.font.get_default_font(), 32)
        textt = fontt.render('Score: ' + str(SCORE), True, (0, 255, 0))
        display.blit(textt, (WIDTH/2, HEIGHT/2))
    
    pygame.display.flip()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        drawWindow()
        updateEntites()
        ball.collision()

        debugging()

        clock.tick(FPS)

loadlevels()

def debugging():
    # print("PLATFORM", platform.rect[0], platform.rect[1])
    # print("BALL", ball.directionX, ball.directionY)
    # print(ball.direction)
    pass

if __name__ == '__main__':
    main()