import random
import pygame
import math
from shared_variables import SharedVariables
from player import Player
from enemy import Enemy
from timer import Timer
from forcemove import ForceMove
from button import Button

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

# Initialize SharedVariables singleton instance
shared_vars = SharedVariables()
shared_vars.warnEnemies = pygame.sprite.Group()
shared_vars.enemies = pygame.sprite.Group()
shared_vars.allEnemies = pygame.sprite.Group() 
shared_vars.gametime = 0
shared_vars.forceMoveTimer = 2000
shared_vars.controls = "WASD"
shared_vars.screen = screen

def win():
    # wait 1 sec
    pygame.time.wait(1000)
    # display win screen
    shared_vars.currentScreen = 'win'

def lose():
    # pause for 1 second
    pygame.time.wait(1000)
    # display the lose screen
    shared_vars.currentScreen = 'gameover'

def wave1():
    gtTrunc = math.floor(shared_vars.gametime)
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
    if shared_vars.gametime <= lv1:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(shared_vars.allEnemies.sprites()):
                shared_vars.allEnemies.add(Enemy('Still', player))
    
    if shared_vars.gametime > lv1 and shared_vars.gametime <= lv2:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(shared_vars.allEnemies.sprites()):
                shared_vars.allEnemies.add(Enemy('LR', player))
                shared_vars.allEnemies.add(Enemy('Still', player))

    if shared_vars.gametime > lv2 and shared_vars.gametime <= lv3:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(shared_vars.allEnemies.sprites()):
                shared_vars.allEnemies.add(Enemy('UD', player))
                shared_vars.allEnemies.add(Enemy('Still', player))

    if shared_vars.gametime > lv3 and shared_vars.gametime <= lv4:
        if gtTrunc % 5 == 0:
            if gtTrunc / 5 == len(shared_vars.allEnemies.sprites()):
                shared_vars.allEnemies.add(Enemy('LRUD', player))
                shared_vars.allEnemies.add(Enemy('Still', player))
# init
player = Player(lose)
# make an enemy
# Enemy()

timer = Timer()
forceMove = ForceMove(lose)
# game loop
running = True
shared_vars.currentScreen = 'main'
# paused = False
while running:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # draw
    screen.fill(background_color)

    shared_vars.dt = clock.tick(600)

    if shared_vars.currentScreen == 'game':

        wave1()

        shared_vars.allEnemies = pygame.sprite.Group()
        for i in shared_vars.warnEnemies.sprites():
            shared_vars.allEnemies.add(i)
        for i in shared_vars.enemies.sprites():
            shared_vars.allEnemies.add(i)

            # update everything
        player.update()
        # if not paused:
        shared_vars.warnEnemies.update()
        shared_vars.enemies.update()
        timer.update()
        forceMove.update()
    elif shared_vars.currentScreen == 'main':
        # a 200 wide and 50 high grey button
        startButton = Button("Start", screen.get_rect().width / 2 - 100, screen.get_rect().height / 2, 200, 50, (100, 100, 100), "start")
        startButton.update()
        # make a settings button below that
        settingsButton = Button("Settings", screen.get_rect().width / 2 - 100, screen.get_rect().height / 2 + 50, 200, 50, (100, 100, 100), "settings")
        settingsButton.update()
    elif shared_vars.currentScreen == 'settings':
        # make a controls button in the middle of the screen
        # it should say "Controls"
        controlsButton = Button("Controls: " + str(shared_vars.controls), screen.get_rect().width / 2 - 100, screen.get_rect().height / 2, 200, 50, (100, 100, 100), "controls")
        controlsButton.update()
        # make a back button at the bottom of the screen that returns to the main screen
        backButton = Button("Back", screen.get_rect().width / 2 - 100, screen.get_rect().height - 50, 200, 50, (100, 100, 100), "main")
        backButton.update()
    elif shared_vars.currentScreen == 'gameover':
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
    elif shared_vars.currentScreen == 'win':
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
