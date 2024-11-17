import pygame
import random
from shared_variables import SharedVariables

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, player_dependency, x=None, y=None):
        pygame.sprite.Sprite.__init__(self)
        self.size = 35
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = [x, y]        # set x and y to a random position if they are not specified
        self.player_dependency = player_dependency
        # if it is touching the player, respawn it
        if x == None:
            self.pos[0] = random.randint(0, SharedVariables().screen.get_size()[0])
        if y == None:
            self.pos[1] = random.randint(0, SharedVariables().screen.get_size()[1])
        
        self.updateRect()
        if self.rect.colliderect(self.player_dependency.rect):
            self.__init__(self.type)
        self.speed = 0.5
        if random.randint(0, 1) == 0:
            self.dir = 1
        else:
            self.dir = -1

        self.warn = 1

        # add to warnEnemies group
        SharedVariables().warnEnemies.add(self)
    
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
            SharedVariables().warnEnemies.remove(self)
            # add to the enemies group
            SharedVariables().enemies.add(self)
            self.warn = -1
        if self.warn == -1:
            self.moveAccordingToType()

        # blit
        SharedVariables().screen.blit(self.image, self.rect)

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
            if self.rect.right > SharedVariables().screen.get_rect().width:
                self.dir = -1
            self.move(self.dir * self.speed * SharedVariables().dt, 0)
                
        elif self.type == 'UD':
            # move up or down
            # bounce this object if touching edge
            if self.rect.y < 0:
                self.dir = 1
            if self.rect.bottom > SharedVariables().screen.get_size()[1]:
                self.dir = -1
            self.move(0, self.dir * self.speed)
        elif self.type == 'LRUD':
            # bounce this object around the screen
            if self.rect.x < 0: # left
                self.dir = 1
            if self.rect.right > SharedVariables().screen.get_rect().width: # right
                self.dir = -1
            if self.rect.y < 0: # up
                self.dir = 2
            if self.rect.bottom > SharedVariables().screen.get_size()[1]: # down
                self.dir = -2
            if self.dir == 1:
                self.move(self.speed * SharedVariables().dt, -self.speed * SharedVariables().dt)
            elif self.dir == -1:
                self.move(-self.speed * SharedVariables().dt, self.speed * SharedVariables().dt)
            elif self.dir == 2:
                self.move(self.speed * SharedVariables().dt, self.speed * SharedVariables().dt)
            elif self.dir == -2:
                self.move(-self.speed * SharedVariables().dt, -self.speed * SharedVariables().dt)

    def move(self, x, y):
        # use a pos variable to store the new position instead of using rect
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        self.updateRect()
    
    def updateRect(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
