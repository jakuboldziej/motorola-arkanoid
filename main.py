from level import *
from editor import *

pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)

# Level management
def loadlevels():
    global WINSCORE, BRICKAMOUNT, level, playing
    level = Level()
    level.draw()
    WINSCORE = level.winscore
    # BRICKAMOUNT += 8
    # print(CURRENTLEVEL, WINSCORE, PREVSCORE)
    playing = True
    main()

def loadNextLevel():
    global CURRENTLEVEL, PREVSCORE, bricks
    CURRENTLEVEL += 1
    PREVSCORE += level.winscore
    ball.stick = True
    for brick in bricks:
        brick.kill()
    # print("next level", CURRENTLEVEL)
    loadlevels()

# Collisions
def manageCollisions():
    # Platform - Ball Collision
    if pygame.sprite.collide_rect(platform, ball):
        ball.direction = ball.direction.split(",")[0] + ",up"
        center = platform.rect[2]//3
        collidePoint = ball.rect[0] + ball.rect[2] - platform.rect[0]
        # XD
        if platform.currentPowerUp == "catchingMode":
            ball.stick = True
        else:
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
    brickCollision = pygame.sprite.spritecollide(ball, bricks, False)
    for brick in brickCollision:
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

        if platform.currentPowerUp == "strongerHit" and brick.color != GOLD:
            brick.health = 0
        else:
            brick.health -= 1

        if brick.health == 0:
            global SCORE
            brick.kill()
            # print(SCORE, PREVSCORE, CURRENTLEVEL * 1000)
            if brick.color != SILVER and SCORE > CURRENTLEVEL * 2000:
                powerUp = PowerUp(brick.rect[0] + brick.rect[2]/2, brick.rect[1] + brick.rect[3]*2, brick.color[0])
                powerUps.add(powerUp)

            SCORE += brick.value
            if SCORE == WINSCORE + PREVSCORE:
                loadNextLevel()

    # Platform - PowerUp Collision
    powerUpCollision = pygame.sprite.spritecollide(platform, powerUps, False)
    for powerUp in powerUpCollision:
        powerUp.boost()
        powerUp.kill()

# Drawing and updating
def drawText():
    text1 = font.render('Score: ' + str(SCORE), True, (0, 255, 0))
    text2 = font.render('Level: ' + str(CURRENTLEVEL), True, (0, 255, 0))
    text3 = font.render('Lifes: ' + str(platform.lifes), True, (0, 255, 0))
    display.blit(text1, (10, 10))
    display.blit(text2, (WIDTH-150, 10))
    display.blit(text3, (10, 50))

def drawWindow():
    display.blit(background, (0, 0))
    for brick in bricks:
        display.blit(brick.surf, brick.rect)
        brick.draw()

    for powerUp in powerUps:
        display.blit(powerUp.surf, powerUp.rect)

    display.blit(platform.surf, platform.rect)

    ball.draw()
    platform.draw()

    drawText()

    pygame.display.flip()

def updateEntites():
    pressed_keys = pygame.key.get_pressed()

    for powerUp in powerUps:
        powerUp.update()

    platform.update(pressed_keys)
    ball.update()

def restartBall():
    platform.rect.x = WIDTH/2
    platform.rect.y = HEIGHT-25
    ball.stick = True
    main()

def manageLifes():
    global CURRENTLEVEL, SCORE, PREVSCORE
    if platform.lifes == 0:
        CURRENTLEVEL = 1
        SCORE = 0
        PREVSCORE = 0
        platform.rect[2] = 100
        # do something

# Game Loops
def howToPlay():
    running = True
    while running:
        display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu()
                    running = False
            if event.type == QUIT:
                quit()

        text1 = font.render('You can move platform by pressing', True, WHITE)
        text2 = font.render('arrow keys on your beyboard.', True, WHITE)
        text3 = font.render('Press spacebar to release the ball.', True, WHITE)
        text4 = font.render('Press escape to stop the game.', True, WHITE)
        text5 = font.render('Brick values:', True, WHITE)
        values = pygame.image.load(path.join(BASEDIR, "images/values.png")).convert()
        display.blit(values, (57, 50))
        display.blit(text1, (WIDTH/6, HEIGHT/3 - 10))
        display.blit(text2, (WIDTH/5 + 20, HEIGHT/2 - 60))
        display.blit(text3, (WIDTH/5 - 15, HEIGHT/1.5 - 80))
        display.blit(text4, (WIDTH/5 + 18, HEIGHT/1.5 - 40))
        display.blit(text5, (WIDTH/3 + 35, 10))
        button3 = Button(WIDTH/2-75, HEIGHT/1.3, 150, 60, buttonText="Back", onclickFunction=mainMenu)
        button3.process()

        pygame.display.flip()
        clock.tick(FPS)

def settings():
    running = True
    while running:
        display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu()
                    running = False
            if event.type == QUIT:
                quit()

        button1 = Button(WIDTH/2-75, HEIGHT/1.3, 150, 60, buttonText="Back", onclickFunction=mainMenu)
        button1.process()

        pygame.display.flip()
        clock.tick(FPS)
                
def editor():
    running = True
    while running:
        global mouse
        mouse = Mouse()
        display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu()
                    running = False
            if event.type == QUIT:
                quit()

        # editor = Editor()
        # display.blit(editor.surf, editor.rect)
        for gridBlock in gridBlocks:
            gridBlock.draw()
            gridBlock.process()

        for choosingGridBlock in choosingGridBlocks:
            choosingGridBlock.draw()
            choosingGridBlock.process()

        button1 = Button(WIDTH/2-75, HEIGHT/1.2, 150, 60, buttonText="Back", onclickFunction=mainMenu)
        button2 = Button(3, HEIGHT-63, 150, 60, buttonText="Save", onclickFunction=mainMenu)
        button1.process()
        button2.process()

        pygame.display.flip()
        clock.tick(FPS)

def mainMenu():
    running = True
    while running:
        display.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

        if playing:
            button1 = Button(WIDTH/2-75, HEIGHT/2-100, 150, 60, buttonText="Resume", onclickFunction=main)
            button5 = Button(WIDTH-153, HEIGHT-63, 150, 60, buttonText="Restart", onclickFunction=restartBall)
            button5.process()
        else:
            button1 = Button(WIDTH/2-75, HEIGHT/2-100, 150, 60, buttonText="Start", onclickFunction=loadlevels)
            button6 = Button(WIDTH-153, HEIGHT-63, 150, 60, buttonText="Editor", onclickFunction=editor)
            button6.process()

        button2 = Button(WIDTH/2-75, HEIGHT/2-30, 150, 60, buttonText="Settings", onclickFunction=settings)
        button3 = Button(WIDTH/2-75, HEIGHT/2+40, 150, 60, buttonText="Exit", onclickFunction=exit)
        button4 = Button(WIDTH-203, 3, 200, 60, buttonText="How To Play", onclickFunction=howToPlay)

        button1.process()
        button2.process()
        button3.process()
        button4.process()

        pygame.display.flip()
        clock.tick(FPS)

def main():
    running = True
    while running:
        display.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu()
                    running = False
            elif event.type == QUIT:
                running = False

        drawWindow()
        updateEntites()
        manageCollisions()

        debugging()

        clock.tick(FPS)

def debugging():
    # print("PLATFORM", platform.rect[0], platform.rect[1])
    # print("BALL", ball.directionX, ball.directionY)
    # print(ball.direction)
    pass

mainMenu()