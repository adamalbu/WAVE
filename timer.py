import pygame
import math
from shared_variables import SharedVariables

class Timer(pygame.sprite.Sprite):
    def __init__(self):
        # text at the top-left
        self.font = pygame.font.Font(None, 30)
        # display the time
    
    def update(self):
        # add 1 to time
        SharedVariables().gametime += 1 / 1000 * (SharedVariables().dt + 0.6)
        # display the time at the bottom-right of the screen
        text = self.font.render(str(math.floor(SharedVariables().gametime)), 1, (255, 0, 255))
        SharedVariables().screen.blit(text, (SharedVariables().screen.get_rect().width - text.get_rect().width, SharedVariables().screen.get_rect().height - text.get_rect().height))
