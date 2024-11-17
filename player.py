import pygame
from shared_variables import SharedVariables
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, lose_callback, speed=0.5):
        pygame.sprite.Sprite.__init__(self)
        self.size = 35
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = SharedVariables().screen.get_rect().centerx
        self.rect.centery = SharedVariables().screen.get_rect().centery
        self.speed = speed
        self.pos = [self.rect.centerx, self.rect.centery]

        self.lose_callback = lose_callback

        self.lastCursorLoc = pygame.mouse.get_pos()
        self.currentCursorLoc = pygame.mouse.get_pos()
        
    def update(self):
        # global paused
        # blit
        SharedVariables().screen.blit(self.image, self.rect)
        # control
        # if not paused: # Paused is never set to True
        self.control()
        # enemy check
        self.enemyCheck()
        # debug last and current mouse position
        # if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            # paused = not paused

    def control(self):
        if SharedVariables().controls == "WASD" or SharedVariables().controls == "arrows":
            # move the player using keys
            keys = pygame.key.get_pressed()
            horizontal_movement = 0
            vertical_movement = 0
            if SharedVariables().controls == "arrows":
                if keys[pygame.K_LEFT]:
                    horizontal_movement = -self.speed
                if keys[pygame.K_RIGHT]:
                    horizontal_movement = self.speed
                if keys[pygame.K_UP]:
                    vertical_movement = -self.speed
                if keys[pygame.K_DOWN]:
                    vertical_movement = self.speed
            if SharedVariables().controls == "WASD":
                if keys[pygame.K_a]:
                    horizontal_movement = -self.speed
                if keys[pygame.K_d]:
                    horizontal_movement = self.speed
                if keys[pygame.K_w]:
                    vertical_movement = -self.speed
                if keys[pygame.K_s]:
                    vertical_movement = self.speed
            if horizontal_movement != 0 and vertical_movement != 0:
                horizontal_movement *= 1 / math.sqrt(2)
                vertical_movement *= 1 / math.sqrt(2)
            self.move(horizontal_movement, vertical_movement)
            if horizontal_movement != 0 or vertical_movement != 0:
                SharedVariables().isPlayerMoving = True
            else:
                SharedVariables().isPlayerMoving = False
        else:
            self.currentCursorLoc = pygame.mouse.get_pos()
            # move the player using mouse
            mouse = pygame.mouse.get_pos()
            self.rect.centerx = mouse[0]
            self.rect.centery = mouse[1]
            # check if the mouse is moving by comparing the last and current mouse position
            if self.lastCursorLoc != self.currentCursorLoc:
                SharedVariables().isPlayerMoving = True
            else:
                SharedVariables().isPlayerMoving = False
            self.lastCursorLoc = self.currentCursorLoc
        # pause if esc pressed

    def move(self, x, y):
        # move using pos
        self.pos[0] += x
        self.pos[1] += y

        # clamp position within screen boundaries
        self.pos[0] = max(self.rect.width / 2, min(self.pos[0], SharedVariables().screen.get_width() - self.rect.width / 2))
        self.pos[1] = max(self.rect.height / 2, min(self.pos[1], SharedVariables().screen.get_height() - self.rect.height / 2))

        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
    
    def enemyCheck(self):
        # check if the player is touching an enemy
        for enemy in SharedVariables().enemies:
            if self.rect.colliderect(enemy.rect):
                # stop the game
                self.lose_callback()
