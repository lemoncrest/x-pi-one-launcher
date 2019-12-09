import pygame
from core.colors import *

class Button():

    rectangle = None
    txt = None
    textPoint = None
    surface = None
    color = None

    def __init__(self,rectangle,txt,textPoint,surface=None,color=COLOR_GRAY,callback=None):
        self.rectangle = rectangle
        self.txt = txt
        self.textPoint = textPoint
        self.surface = surface
        self.color = color
        self.callback = callback

    def draw(self,surface=None):
        targetSurface = self.surface

        if self.surface is None:
            targetSurface = surface

        pygame.draw.rect(targetSurface, self.color, self.rectangle, 0)
        targetSurface.blit(self.txt, self.textPoint )
