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
        self.prev_pos = self.pos.copy()

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
        moving = horizontal_movement != 0 or vertical_movement != 0
        self.move(horizontal_movement, vertical_movement)

    def move(self, x, y):
        # Store previous position
        prev_pos = self.pos.copy()
        # Move using pos
        self.pos[0] += x
        self.pos[1] += y
        # Clamp position within screen boundaries
        min_x = self.rect.width / 2
        max_x = SharedVariables().screen.get_width() - self.rect.width / 2
        min_y = self.rect.height / 2
        max_y = SharedVariables().screen.get_height() - self.rect.height / 2
        clamped_x = max(min_x, min(self.pos[0], max_x))
        clamped_y = max(min_y, min(self.pos[1], max_y))
        # Calculate movement vector
        movement_vector = [clamped_x - prev_pos[0], clamped_y - prev_pos[1]]
        # Update position
        self.pos[0] = clamped_x
        self.pos[1] = clamped_y
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        # Determine if player is moving
        moving = self.pos != prev_pos
        # Check if moving towards the border
        moving_towards_border = (
            (self.pos[0] == min_x and x < 0) or
            (self.pos[0] == max_x and x > 0) or
            (self.pos[1] == min_y and y < 0) or
            (self.pos[1] == max_y and y > 0)
        )
        # Set isPlayerMoving
        SharedVariables().isPlayerMoving = moving and not moving_towards_border
    
    def enemyCheck(self):
        # check if the player is touching an enemy
        for enemy in SharedVariables().enemies:
            if self.rect.colliderect(enemy.rect):
                # stop the game
                self.lose_callback()
