from classes import *
from level import *

pygame.init()

# Level management
def loadlevels():
    level1()

# Collisions
def manageCollisions():
    # Platform - Ball Collision
    if pygame.sprite.collide_rect(platform, ball):
        ball.direction = ball.direction.split(",")[0] + ",up"
        center = platform.rect[2]//3
        collidePoint = ball.rect[0] + ball.rect[2] - platform.rect[0]
        # XD
        if center < collidePoint < center*2:
            if platform.platformDirection == "left":
                ball.directionX = -5
            elif platform.platformDirection == "right":
                ball.directionX = 5
        elif collidePoint > center*2:
            if platform.platformDirection == "left":
                ball.directionX = -3
            elif platform.platformDirection == "right":
                ball.directionX = 3
        else:
            if platform.platformDirection == "left":
                ball.directionX = -3
            elif platform.platformDirection == "right":
                ball.directionX = 3
            
        ball.directionY = -ball.speedY
        ball.rect.move_ip(ball.directionX, ball.directionY)

    # Brick - Ball Collision
    collision = pygame.sprite.spritecollide(ball, bricks, False)
    for brick in collision:
        if ball.rect.left < brick.rect.right and ball.direction.split(",")[0] == "left" and not ball.rect.right < brick.rect.right:
            ball.directionX = +ball.speedX
            # print(self.direction.split(","), "RIGHT")
        elif ball.rect.right > brick.rect.left and ball.direction.split(",")[0] == "right" and not ball.rect.left > brick.rect.left:
            ball.directionX = -ball.speedX
            # print(self.direction.split(","), "LEFT")
        elif ball.rect.top < brick.rect.bottom and ball.rect.bottom > brick.rect.bottom:
            ball.directionY = +ball.speedY
            # print(self.direction.split(","), "BOTTOM")
        elif ball.rect.bottom > brick.rect.top and ball.direction.split(",")[1] == "down":
            ball.directionY = -ball.speedY
            # print(self.direction.split(","), "TOP")
        brick.kill()
        global SCORE
        SCORE += 10

font = pygame.font.Font(pygame.font.get_default_font(), 32)

# Drawing and updating
def drawScore():
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

# Main Loops
def mainMenu():
    running = True
    while running:
        display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        button1 = Button(WIDTH/2-50, HEIGHT/2-50, 150, 60, buttonText="Start", onclickFunction=main)
        button2 = Button(WIDTH/2-50, HEIGHT/2+20, 150, 60, buttonText="Settings", onclickFunction=exit)
        button3 = Button(WIDTH/2-50, HEIGHT/2+90, 150, 60, buttonText="Exit", onclickFunction=exit)

        button1.process()
        button2.process()
        button3.process()

        pygame.display.flip()
        clock.tick(FPS)

def main():
    running = True
    while running:
        display.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        drawWindow()
        updateEntites()
        manageCollisions()

        debugging()

        clock.tick(FPS)

loadlevels()

def debugging():
    # print("PLATFORM", platform.rect[0], platform.rect[1])
    # print("BALL", ball.directionX, ball.directionY)
    # print(ball.direction)
    pass

if __name__ == '__main__':
    mainMenu()