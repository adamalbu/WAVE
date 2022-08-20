from distutils.log import warn
import random
import pygame
import math

# init pygame
pygame.init()
# set the screen size to a square
screen = pygame.display.set_mode((500, 500))
# set the title of the window to WAVE
pygame.display.set_caption("WAVE")
# set the background color to black
background_color = (0, 0, 0)

# set the fps to 30
clock = pygame.time.Clock()

warnEnemies = pygame.sprite.Group()
enemies = pygame.sprite.Group()
allEnemies = pygame.sprite.Group()
gametime = 0
forceMoveTimer = 2000
controls = "WASD"

# region Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, speed=0.5):
        pygame.sprite.Sprite.__init__(self)
        self.size = 35
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen.get_rect().centerx
        self.rect.centery = screen.get_rect().centery
        self.speed = speed
        self.pos = [self.rect.centerx, self.rect.centery]

        self.lastCursorLoc = pygame.mouse.get_pos()
        self.currentCursorLoc = pygame.mouse.get_pos()
        
    def update(self):
        # global paused
        # blit
        screen.blit(self.image, self.rect)
        # control
        if not paused:
            self.control()
        # enemy check
        self.enemyCheck()
        # debug last and current mouse position
        # if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            # paused = not paused

    def control(self):
        global isPlayerMoving
        if controls == "WASD" or controls == "arrows":
            # move the player using keys
            if controls == "arrows":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.move(-self.speed, 0)
                if keys[pygame.K_RIGHT]:
                    self.move(self.speed, 0)
                if keys[pygame.K_UP]:
                    self.move(0, -self.speed)
                if keys[pygame.K_DOWN]:
                    self.move(0, self.speed)
                # check if any arrow is pressed
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    isPlayerMoving = True
                else:
                    isPlayerMoving = False
            # move the player using w a s d
            if controls == "WASD":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.move(-self.speed, 0)
                if keys[pygame.K_d]:
                    self.move(self.speed, 0)
                if keys[pygame.K_w]:
                    self.move(0, -self.speed)
                if keys[pygame.K_s]:
                    self.move(0, self.speed)
                # check if any key is pressed
                if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                    isPlayerMoving = True
                else:
                    isPlayerMoving = False
        else:
            self.currentCursorLoc = pygame.mouse.get_pos()
            # move the player using mouse
            mouse = pygame.mouse.get_pos()
            self.rect.centerx = mouse[0]
            self.rect.centery = mouse[1]
            # check if the mouse is moving by comparing the last and current mouse position
            if self.lastCursorLoc != self.currentCursorLoc:
                isPlayerMoving = True
            else:
                isPlayerMoving = False
            self.lastCursorLoc = self.currentCursorLoc
        # pause if esc pressed

    def move(self, x, y):
        # move using pos
        self.pos[0] += x
        self.pos[1] += y

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        # check if the player is touching the screen borders
        # if they are, stop the player
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen.get_rect().right:
            self.rect.right = screen.get_rect().right
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen.get_rect().bottom:
            self.rect.bottom = screen.get_rect().bottom
    
    def enemyCheck(self):
        # check if the player is touching an enemy
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                # stop the game
                lose()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, x=None, y=None):
        pygame.sprite.Sprite.__init__(self)
        self.size = 35
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = [x, y]        # set x and y to a random position if they are not specified
        # if it is touching the player, respawn it
        if x == None:
            self.pos[0] = random.randint(0, screen.get_size()[0])
        if y == None:
            self.pos[1] = random.randint(0, screen.get_size()[1])
        
        self.updateRect()
        if self.rect.colliderect(player.rect):
            self.__init__(self.type)
        self.speed = 0.5
        if random.randint(0, 1) == 0:
            self.dir = 1
        else:
            self.dir = -1

        self.warn = 1

        # add to warnEnemies group
        warnEnemies.add(self)
    
    def update(self):
        self.applyColorAccordingToType()
        if self.warn < 200 and not self.warn == -1:
            self.warn -= 1
            # set the alpha of the enemy to the warn level
            self.image.set_alpha(self.warn)
            self.warn += 1.3
        elif self.warn >= 200:
            self.image.set_alpha(255)
            # remove from warnEnemies group
            warnEnemies.remove(self)
            # add to the enemies group
            enemies.add(self)
            self.warn = -1
        if self.warn == -1:
            self.moveAccordingToType()

        # blit
        screen.blit(self.image, self.rect)

    def applyColorAccordingToType(self):
        if self.type == 'LR':
            self.image.fill((0, 255, 0))
        elif self.type == 'UD':
            self.image.fill((0, 0, 255))
        elif self.type == 'LRUD':
            self.image.fill((0, 255, 255))

    def moveAccordingToType(self):
        if self.type == 'LR':
            # move left or right
            # bounce this object if touching edge
            if self.rect.x < 0:
                self.dir = 1
            if self.rect.right > screen.get_rect().width:
                self.dir = -1
            self.move(self.dir * self.speed * dt, 0)
                
        elif self.type == 'UD':
            # move up or down
            # bounce this object if touching edge
            if self.rect.y < 0:
                self.dir = 1
            if self.rect.bottom > screen.get_size()[1]:
                self.dir = -1
            self.move(0, self.dir * self.speed)
        elif self.type == 'LRUD':
            # bounce this object around the screen
            if self.rect.x < 0:
                self.dir = 1
            if self.rect.right > screen.get_rect().width:
                self.dir = -1
            if self.rect.y < 0:
                self.dir = 2
            if self.rect.bottom > screen.get_size()[1]:
                self.dir = -2
            if self.dir == 1:
                self.move(self.speed * dt, 0)
            elif self.dir == -1:
                self.move(-self.speed * dt, 0)
            elif self.dir == 2:
                self.move(0, self.speed * dt)
            elif self.dir == -2:
                self.move(0, -self.speed * dt)

    def move(self, x, y):
        # use a pos variable to store the new position instead of using rect
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        self.updateRect()
    
    def updateRect(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

class Timer(pygame.sprite.Sprite):
    def __init__(self):
        # text at the top-left
        self.font = pygame.font.Font(None, 30)
        # display the time
    
    def update(self):
        # add 1 to time
        global gametime
        gametime += 1 / 1000 * (dt + 0.6)
        # display the time at the bottom-right of the screen
        text = self.font.render(str(math.floor(gametime)), 1, (255, 0, 255))
        screen.blit(text, (screen.get_rect().width - text.get_rect().width, screen.get_rect().height - text.get_rect().height))

class ForceMove(pygame.sprite.Sprite):
    def __init__(self, startValue=2000):
        global forceMoveTimer
        self.startValue = startValue
        self.font = pygame.font.Font(None, 30)
    
    def update(self):
        global forceMoveTimer
        if forceMoveTimer <= 0:
            # stop the game
            lose()
        else:
            if gametime > 2:
                global isPlayerMoving
                if isPlayerMoving:
                    if forceMoveTimer >= self.startValue:
                        # reset the timer
                        forceMoveTimer = self.startValue
                    else:
                        if controls == "mouse":
                            forceMoveTimer += 5 * dt
                        else:
                            forceMoveTimer += 2 * dt
                else:   
                    forceMoveTimer -= 1 * dt

        self.display()
    # display text at bottom-left of screen
    def display(self):
        text = self.font.render(str(forceMoveTimer), 1, (255, 0, 255))
        screen.blit(text, (0, screen.get_rect().height - text.get_rect().height))

class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width=200, height=50, color=(100, 100, 100), action=None):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.action = action
        
        # draw the button
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # blit

        # draw the text
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(self.text, 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = self.rect.centerx
        self.textpos.centery = self.rect.centery

    def update(self):
        # check if mouse is over the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # change the opacity of the button
            self.image.set_alpha(100)
            # check if mouse is clicked
            if pygame.mouse.get_pressed()[0]:
                self.runAction()
        else:
            self.image.set_alpha(255)

        # blit
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textpos)

    def runAction(self):
        global currentScreen
        if self.action == "start":
            global gametime
            gametime = 0
            # reset forceMoveTimer
            global forceMoveTimer
            forceMoveTimer = 2000
            # erase all enemies
            allEnemies.empty()
            enemies.empty()
            warnEnemies.empty()            
            # start the game
            currentScreen = 'game'
        elif self.action == "controls":
            global controls
            if controls == "WASD":
                controls = "arrows"
            elif controls == "arrows":
                controls = "mouse"
            elif controls == "mouse":
                controls = "WASD"
            # pause for 0.1 seconds
            pygame.time.wait(100)
        else:
            currentScreen = self.action
# endregion

def win():
    # wait 1 sec
    pygame.time.wait(1000)
    # display win screen
    global currentScreen
    currentScreen = 'win'

def lose():
    # pause for 1 second
    pygame.time.wait(1000)
    # display the lose screen
    global currentScreen
    currentScreen = 'gameover'

def wave1():
    gtTrunc = math.floor(gametime)
    lv1 = 20
    lv2 = 30
    lv3 = 40
    lv4 = 45
    end = 60
    # wave 1
    # create enemies
    # every 5 seconds, create an enemy
    if gtTrunc >= end:
        win()
    if gametime <= lv1:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(allEnemies.sprites()):
                Enemy('Still')
    
    if gametime > lv1 and gametime <= lv2:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(allEnemies.sprites()):
                Enemy('LR')
                Enemy('Still')

    if gametime > lv2 and gametime <= lv3:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(allEnemies.sprites()):
                Enemy('UD')
                Enemy('Still')

    if gametime > lv3 and gametime <= lv4:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(allEnemies.sprites()):
                Enemy('LRUD')
                Enemy('Still')
# init
player = Player()
# make an enemy
# Enemy()

timer = Timer()
forceMove = ForceMove()
# game loop
running = True
currentScreen = 'main'
paused = False
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # draw
    screen.fill(background_color)

    dt = clock.tick()

    if currentScreen == 'game':

        wave1()

        allEnemies = pygame.sprite.Group()
        for i in warnEnemies.sprites():
            allEnemies.add(i)
        for i in enemies.sprites():
            allEnemies.add(i)

            # update everything
        player.update()
        if not paused:
            warnEnemies.update()
            enemies.update()
            timer.update()
            forceMove.update()
    elif currentScreen == 'main':
        # a 200 wide and 50 high grey button
        startButton = Button("Start", screen.get_rect().width / 2 - 100, screen.get_rect().height / 2, 200, 50, (100, 100, 100), "start")
        startButton.update()
        # make a settings button below that
        settingsButton = Button("Settings", screen.get_rect().width / 2 - 100, screen.get_rect().height / 2 + 50, 200, 50, (100, 100, 100), "settings")
        settingsButton.update()
    elif currentScreen == 'settings':
        # make a controls button in the middle of the screen
        # it should say "Controls" then the controls
        controlsButton = Button("Controls: " + str(controls), screen.get_rect().width / 2 - 100, screen.get_rect().height / 2, 200, 50, (100, 100, 100), "controls")
        controlsButton.update()
        # make a back button at the bottom of the screen that returns to the main screen
        backButton = Button("Back", screen.get_rect().width / 2 - 100, screen.get_rect().height - 50, 200, 50, (100, 100, 100), "main")
        backButton.update()
    elif currentScreen == 'gameover':
        # display game over at the top
        gameoverText = pygame.font.Font(None, 100).render("Game Over", 1, (255, 255, 255))
        gameoverTextpos = gameoverText.get_rect()
        gameoverTextpos.centerx = screen.get_rect().centerx
        gameoverTextpos.centery = screen.get_rect().centery - 50
        screen.blit(gameoverText, gameoverTextpos)

        # make a restart button in the middle of the screen
        restartButton = Button("Restart", screen.get_rect().width / 2 - 100, screen.get_rect().height / 2, 200, 50, (100, 100, 100), "start")
        restartButton.update()
        # make a back button at the bottom of the screen that returns to the main screen
        backButton = Button("Back", screen.get_rect().width / 2 - 100, screen.get_rect().height - 50, 200, 50, (100, 100, 100), "main")
        backButton.update()
    elif currentScreen == 'win':
        # display you win over at the top
        winText = pygame.font.Font(None, 100).render("You Win!", 1, (255, 255, 255))
        winTextpos = winText.get_rect()
        winTextpos.centerx = screen.get_rect().centerx
        winTextpos.centery = screen.get_rect().centery - 50
        screen.blit(winText, winTextpos)


        # make a restart button in the middle of the screen
        restartButton = Button("Play Again", screen.get_rect().width / 2 - 100, screen.get_rect().height / 2, 200, 50, (100, 100, 100), "start")
        restartButton.update()
        # make a back button at the bottom of the screen that returns to the main screen
        backButton = Button("Back", screen.get_rect().width / 2 - 100, screen.get_rect().height - 50, 200, 50, (100, 100, 100), "main")
        backButton.update()

    pygame.display.flip()
