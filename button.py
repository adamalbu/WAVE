import pygame
from shared_variables import SharedVariables

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
        SharedVariables().screen.blit(self.image, self.rect)
        SharedVariables().screen.blit(self.text, self.textpos)

    def runAction(self):
        if self.action == "start":
            SharedVariables().gametime = 0
            # reset forceMoveTimer
            SharedVariables().forceMoveTimer = 2000
            # erase all enemies
            SharedVariables().allEnemies.empty()
            SharedVariables().enemies.empty()
            SharedVariables().warnEnemies.empty()            
            # start the game
            SharedVariables().currentScreen = 'game'
        elif self.action == "controls":
            if SharedVariables().controls == "WASD":
                SharedVariables().controls = "arrows"
            elif SharedVariables().controls == "arrows":
                SharedVariables().controls = "WASD"
            # pause for 0.1 seconds
            pygame.time.wait(100)
        else:
            SharedVariables().currentScreen = self.action  # Update the SharedVariables instance