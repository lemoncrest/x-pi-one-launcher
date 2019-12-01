# coding=utf-8
import pygame
import os
from core.colors import *
from core.utils import Utils

WINDOW_SIZE = (1024, 600)
ALPHA = 192
BARSIZE = 60
FONT_SIZE = 20


class UpBar():

    def __init__(self,surface):
        self.surface = surface # main screen
        self.bar = pygame.Surface((WINDOW_SIZE[0], BARSIZE), pygame.SRCALPHA)
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assert/fonts","DejaVuSans.ttf"), FONT_SIZE)

    def draw(self):
        self.drawBackground()
        self.drawMenuButton()

    def drawMenuButton(self):
        self.menu = Utils.drawRectangleButton(
            text="Todo lo que tiene un principio tiene un final",
            font=self.font,surface=self.surface,
            fillHeight= True,
            fillWidth = False,
            centeredY = True,
            centeredX = False,
            margin = 0,
            padding = 0,
            parentSize=(WINDOW_SIZE[0],60))

    def drawBackground(self):
        # add alpha to tuple {transform (,,,) to (,,,,ALPHA)}
        black_with_alpha = COLOR_BLACK + (ALPHA, )
        pygame.draw.rect(self.bar, black_with_alpha, (0,0, WINDOW_SIZE[0],BARSIZE))
        self.surface.blit(self.bar,(0,0))
