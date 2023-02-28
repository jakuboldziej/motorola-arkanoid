from level import *

pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)

# Level management
def loadlevels():
    global level, playing
    level = Level()
    level.draw()
    print(playing, platform.currentLevel, level.winscore, PREVSCORE, SCORE)
    if level.brickArray:
        playing = True
        main()

def loadNextLevel():
    global PREVSCORE, bricks, platform
    ball.directionX = 0
    ball.directionY = 0
    ball.rect[0] = platform.rect[0] + platform.rect[2]/2 - ball.rect[2]/2
    ball.rect[1] = platform.rect[1] - 25
    ball.stick = True
    platform.currentLevel += 1
    PREVSCORE += level.winscore
    level.winscore = 0
    for brick in bricks:
        brick.kill()
    print("next level", platform.currentLevel)
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
            ball.direction = "right," + ball.direction.split(",")[1]
        elif ball.rect.right > brick.rect.left and ball.direction.split(",")[0] == "right" and not ball.rect.left > brick.rect.left:
            ball.directionX = -ball.speedX
            ball.direction = "left," + ball.direction.split(",")[1]
        elif ball.rect.top < brick.rect.bottom and ball.rect.bottom > brick.rect.bottom:
            ball.directionY = +ball.speedY
            ball.direction = ball.direction.split(",")[0] + ",down"
        elif ball.rect.bottom > brick.rect.top and ball.direction.split(",")[1] == "down":
            ball.directionY = -ball.speedY
            ball.direction = ball.direction.split(",")[0] + ",up"
    
        # print(ball.direction)

        if platform.currentPowerUp == "strongerHit" and brick.color != GOLD:
            brick.health = 0
        else:
            if brick.color != GOLD:
                brick.health -= 1

        if brick.health == 0:
            global SCORE
            brick.kill()
            # print(SCORE, PREVSCORE, platform.currentLevel * 1000)
            if brick.color != SILVER and SCORE > platform.currentLevel * 2000:
                powerUp = PowerUp(brick.rect[0] + brick.rect[2]/2, brick.rect[1] + brick.rect[3]*2, brick.color[0])
                powerUps.add(powerUp)

            SCORE += brick.value
            if SCORE - PREVSCORE == level.winscore:
                loadNextLevel()

    # Platform - PowerUp Collision
    powerUpCollision = pygame.sprite.spritecollide(platform, powerUps, False)
    for powerUp in powerUpCollision:
        powerUp.boost()
        powerUp.kill()

# Drawing and updating
def drawText():
    text1 = font.render(f'Score: {str(SCORE)}', True, (0, 255, 0))
    text2 = font.render(f'Level: {str(platform.currentLevel)}', True, (0, 255, 0))
    text3 = font.render(f'Lifes: {str(platform.lifes)}', True, (0, 255, 0))
    display.blit(text1, (10, 10))
    display.blit(text2, (WIDTH-150, 10))
    display.blit(text3, (10, 50))
    # print(platform.currentLevel, SCORE, PREVSCORE, level.winscore)

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
    platform.rect.x = WIDTH/2-50
    platform.rect.y = HEIGHT-45
    ball.stick = True
    main()

# Game Loops
def howToPlay():
    text1 = font.render('Brick values:', True, WHITE[0])
    text2 = font.render('Silver blocks: 50 * level number.', True, WHITE[0])
    text3 = font.render('Gold blocks are indestructible.', True, WHITE[0])
    text4 = font.render('Silver blocks needs 2 hits to brake and extra hit is needed every 8 levels.', True, WHITE[0])
    text5 = font.render('You can move platform by pressing arrow keys on your keyboard', True, WHITE[0])
    text6 = font.render('or by moving your mouse.', True, WHITE[0])
    text7 = font.render('Press spacebar to release the ball.', True, WHITE[0])
    text8 = font.render('Press escape to stop the game.', True, WHITE[0])

    running = True
    while running:
        display.fill(BLACK[0])
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    mainMenu()
            if event.type == QUIT:
                quit()

        display.blit(text1, (WIDTH/2-text1.get_width()/2, 10))
        display.blit(text2, (WIDTH/2-text2.get_width()/2, 120))
        display.blit(text3, (WIDTH/2-text3.get_width()/2, 120 + 50))
        display.blit(text4, (WIDTH/2-text4.get_width()/2, 120 + 50*2))
        display.blit(text5, (WIDTH/2-text5.get_width()/2, 120 + 50*3))
        display.blit(text6, (WIDTH/2-text6.get_width()/2, 120 + 50*4))
        display.blit(text7, (WIDTH/2-text7.get_width()/2, 120 + 50*5))
        display.blit(text8, (WIDTH/2-text8.get_width()/2, 120 + 50*6))

        values = pygame.image.load(path.join(BASEDIR, "images/values.png")).convert()
        display.blit(values, (WIDTH/2-values.get_width()/2, 50))
        
        button1 = Button(WIDTH/2-75, HEIGHT/1.3, 150, 60, buttonText="Back", onclickFunction=mainMenu)
        button1.process()
        button1.draw()

        pygame.display.flip()
        clock.tick(FPS)

def howToEditor():
    running = True
    while running:
        display.fill(BLACK[0])
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    mainMenu()
            if event.type == QUIT:
                quit()

        text1 = font.render('You can choose brick\'s color', True, WHITE[0])
        text2 = font.render('Each block has different value', True, WHITE[0])
        text3 = font.render('50    60     70     80     90     100     110   120', True, WHITE[0])
        display.blit(text1, (WIDTH/2-text1.get_width()/2, 20))
        display.blit(text2, (WIDTH/2-text2.get_width()/2, 150))
        display.blit(text3, (WIDTH/2-text3.get_width()/2, 120))

        values = pygame.image.load(path.join(BASEDIR, "images/choosingGridBlocks.png")).convert()
        display.blit(values, (WIDTH/2-values.get_width()/2, 50))

        button1 = Button(WIDTH/2-75, HEIGHT/1.3, 150, 60, buttonText="Back", onclickFunction=editor)
        button1.process()
        button1.draw()

        pygame.display.flip()
        clock.tick(FPS)

def settingsLoop():
    button1 = Button(WIDTH/2-75, HEIGHT/1.3, 160, 60, buttonText="Back", onclickFunction=mainMenu)
    button2 = Button(WIDTH/10 + 200, HEIGHT/7, 150, 60, buttonText="Change", onclickFunction=changeSteeringType, onePress=True)

    running = True
    while running:
        display.fill(BLACK[0])
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    mainMenu()
            if event.type == QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button1.process()
                button2.process()

        text1 = font.render(f'Platform is controlled by: {settings.steeringType}.', True, (255, 255, 255))
        display.blit(text1, (WIDTH/10, HEIGHT/12))
        
        button1.draw()
        button2.draw()
        
        pygame.display.flip()
        clock.tick(FPS)
                
def editor():
    # inputBox = InputBox(300, 0, 50, 32)
    editorClass.creatingGrid()
    # print(editorClass.currentLevel)

    button1 = Button(WIDTH/2-75, HEIGHT/1.2, 150, 60, buttonText="Back", onclickFunction=mainMenu)
    button2 = Button(3, HEIGHT-63, 150, 60, buttonText="Save", onclickFunction=saveEditor)
    button3 = Button(WIDTH - 147, 50, 30, 30, buttonText="<", onclickFunction=loadPrevEditorLevel, onePress=True)
    button4 = Button(WIDTH - 60, 50, 30, 30, buttonText=">", onclickFunction=loadNextEditorLevel, onePress=True)
    # button5 = Button(WIDTH/2-75, 20, 150, 60, buttonText="Delete", onclickFunction=deleteEditorLevel, onePress=True)
    # button6 = Button(WIDTH/2, 20, 150, 60, buttonText="Clear", onclickFunction=clearEditorLevel, onePress=True)
    button7 = Button(3, 3, 150, 60, buttonText="Help", onclickFunction=howToEditor, onePress=True)

    running = True
    while running:
        global mouse
        mouse = Mouse()
        display.fill(BLACK[0])
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    mainMenu()
            if event.type == QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button1.process()
                button2.process()
                button3.process()
                button4.process()
                # button5.process()
                # button6.process()
                button7.process()
            # inputBox.handle_event(event)

        # print(editorClass.currentLevel)

        for gridBlock in gridBlocks:
            gridBlock.draw()
            gridBlock.process()

        for choosingGridBlock in choosingGridBlocks:
            choosingGridBlock.draw()
            choosingGridBlock.process()

        button1.draw()
        button2.draw()
        button3.draw()
        button4.draw()
        # button5.draw()
        # button6.draw()
        button7.draw()

        text2 = font.render(f'Level: {str(editorClass.currentLevel)}', True, (0, 255, 0))
        display.blit(text2, (WIDTH-150, 10))

        # inputBox.draw(display)

        pygame.display.flip()
        clock.tick(FPS)

def mainMenu():    
    button6 = Button(WIDTH/2-75, HEIGHT-63, 150, 60, buttonText="Editor", onclickFunction=editor)
    
    button2 = Button(WIDTH/2-75, HEIGHT/2-30, 150, 60, buttonText="Settings", onclickFunction=settingsLoop)
    button3 = Button(WIDTH/2-75, HEIGHT/2+40, 150, 60, buttonText="Exit", onclickFunction=exit)
    button4 = Button(WIDTH-203, 3, 200, 60, buttonText="How To Play", onclickFunction=howToPlay)

    running = True
    while running:
        display.fill(BLACK[0])
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

        mouse.update()

        if playing:
            button1 = Button(WIDTH/2-75, HEIGHT/2-100, 150, 60, buttonText="Resume", onclickFunction=main)
            button5 = Button(WIDTH-153, HEIGHT-63, 150, 60, buttonText="Restart", onclickFunction=restartBall)
            button5.process()
            button5.draw()
        else:
            button1 = Button(WIDTH/2-75, HEIGHT/2-100, 150, 60, buttonText="Start", onclickFunction=loadlevels)

        button1.process()
        button2.process()
        button3.process()
        button4.process()
        button6.process()
        button1.draw()
        button2.draw()
        button3.draw()
        button4.draw()
        button6.draw()

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
                    mainMenu()
            elif event.type == QUIT:
                running = False
                quit()
            elif event.type == pygame.MOUSEMOTION:
                if event.rel[0] > 0:
                    platform.platformDirection = "right"
                elif event.rel[0] < 0:
                    platform.platformDirection = "left"
                else:
                    platform.platformDirection = "center"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if settings.steeringType == "mouse":
                    platform.releaseBall()

        if platform.lifes == 0:
            running = False
            gameOver()

        drawWindow()
        updateEntites()
        manageCollisions()

        clock.tick(FPS)

def gameOver():
    global playing, SCORE, PREVSCORE
    button1 = Button(WIDTH/2-75, HEIGHT/1.2, 150, 60, buttonText="Back", onclickFunction=mainMenu)

    for brick in bricks:
        brick.kill()

    platform.lifes = 3
    SCORE = 0
    PREVSCORE = 0
    playing = False
    running = True
    platform.currentLevel = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()  
    
        button1.process()
        button1.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

# Utils
def loadPrevEditorLevel():
    with open("levels.json", "r+") as f:
        data = json.load(f)
        levels = data["levels"]
    if levels:
        if editorClass.currentLevel != 1:
            editorClass.editing = True
            editorClass.currentLevel -= 1
            editor()

def loadNextEditorLevel():
    with open("levels.json", "r+") as f:
        data = json.load(f)
        levels = data["levels"]

    if editorClass.currentLevel < len(levels):
        editorClass.currentLevel += 1
        editorClass.editing = True
    else:
        editorClass.currentLevel = len(levels) + 1
        editorClass.editing = False

    editor()

def deleteEditorLevel():
    with open("levels.json", "r+") as f:
        data = json.load(f)
        levels = data["levels"]

    for level in levels:
        if level["levelId"] == editorClass.currentLevel and editorClass.editing:
            levels.remove(level)

            jsonLevels = json.dumps(data, indent=1)
            with open('levels.json', "w") as f:
                f.write(str(jsonLevels))
            
            editorClass.resetArray()
            editorClass.editing = False
            editor()

def saveEditor():
    with open("levels.json", "r+") as f:
        data = json.load(f)
        levels = data["levels"]

    if levels:
        lastLevelId = levels[-1]["levelId"]
    else:
        lastLevelId = 0
    
    if not editorClass.editing:
        newLevel = {"levelId": int(lastLevelId)+1, "gridArray": editorClass.editingGridBlockArray}
        levels.append(newLevel)
    else:
        editingLevel = levels[editorClass.currentLevel-1]
        editingLevel["gridArray"] = editorClass.editingGridBlockArray

    jsonLevels = json.dumps(data, indent=1)
    with open('levels.json', "w") as f:
        f.write(str(jsonLevels))

    editorClass.editing = True

def clearEditorLevel():
    editorClass.resetArray()

def changeSteeringType():
    if settings.steeringType == "mouse":
        settings.steeringType = "keyboard"
    else:
        settings.steeringType = "mouse"
    # print(settings.steeringType)

def manageLifes():
    global SCORE, PREVSCORE
    if platform.lifes == 0:
        platform.currentLevel = 1
        SCORE = 0
        PREVSCORE = 0
        platform.rect[2] = 100
        # do something

mainMenu()