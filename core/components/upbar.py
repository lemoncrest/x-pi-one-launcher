# coding=utf-8
import pygame
import os
from core.colors import *
from core.utils import Utils
from core.components.menu import Menu

WINDOW_SIZE = (1024, 600)
ALPHA = 192
BARSIZE = 60
FONT_SIZE = 20

class UpBar():

    def __init__(self,surface):
        self.surface = surface # main screen
        self.bar = pygame.Surface((WINDOW_SIZE[0], BARSIZE), pygame.SRCALPHA)
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assert/fonts","DejaVuSans.ttf"), FONT_SIZE)
        self.menu = Menu(title="Menu", first=(0,0) ,parent=(WINDOW_SIZE[0],BARSIZE), font=self.font, surface=self.surface)

    def draw(self):
        self.drawBackground()
        self.menu.draw()

    def drawBackground(self):
        # add alpha to tuple {transform (,,,) to (,,,,ALPHA)}
        black_with_alpha = COLOR_BLACK + (ALPHA, )
        pygame.draw.rect(self.bar, black_with_alpha, (0,0, WINDOW_SIZE[0],BARSIZE))
        self.surface.blit(self.bar,(0,0))
