import pygame
from core.utils import Utils
from core.colors import *
from core.components.button import Button

class Menu():

    title = None
    first = None
    parent = None
    font = None
    surface = None
    mainButton = None

    def __init__(self,title,first,parent,font,surface):
        self.title = title
        self.first = first
        self.parent = parent
        self.font = font
        self.surface = surface

    def draw(self):
        self.mainButton = Utils.getRectangleButton(
            text = self.title,
            font = self.font,
            surface = self.surface,
            fillHeight = False,
            fillWidth = False,
            centeredY = True,
            centeredX = False,
            margin = 5,
            padding = 3,
            parentSize = self.parent
        )
        self.mainButton.draw()
