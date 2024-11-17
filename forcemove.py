import pygame
from shared_variables import SharedVariables

class ForceMove(pygame.sprite.Sprite):
    def __init__(self, lose_callback, startValue=2000):
        self.startValue = startValue
        self.font = pygame.font.Font(None, 30)
        self.lose_callback = lose_callback
    
    def update(self):
        if SharedVariables().forceMoveTimer <= 0:
            self.lose_callback()
        else:
            if SharedVariables().gametime > 2:
                if SharedVariables().isPlayerMoving:
                    if SharedVariables().forceMoveTimer >= self.startValue:
                        SharedVariables().forceMoveTimer = self.startValue
                    else:
                        if SharedVariables().controls == "mouse":
                            SharedVariables().forceMoveTimer += 5 * SharedVariables().dt
                        else:
                            SharedVariables().forceMoveTimer += 2 * SharedVariables().dt
                else:   
                    SharedVariables().forceMoveTimer -= 1 * SharedVariables().dt

        self.display()

    def display(self):
        text = self.font.render(str(SharedVariables().forceMoveTimer), 1, (255, 0, 255))
        SharedVariables().screen.blit(text, (0, SharedVariables().screen.get_rect().height - text.get_rect().height))
