import pygame

from core.constants import *
from core.card.abstractcard import AbstractCard
from core.colors import *
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WifiCard(AbstractCard):

    def __init__(self,surface,padding,font,element,parent=None):
        self.surface = surface
        self.padding = padding
        self.font = font
        self.element = element
        self.parent = parent

    def displayCard(self, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=5):

        grid = (2,2) # card grid

        # fill image
        button_rect = pygame.Rect(x, y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

        if selected_field:
            # draw background rectangle
            button_rect_background = pygame.Rect(x + selected_margin, y + selected_margin,
            (sizeX / grid[0]) - selected_margin * 2,
            sizeY - selected_margin * 2)
            pygame.draw.rect(self.surface, COLOR_BLUE, button_rect_background, 0)

        # fill title
        button_rect = pygame.Rect(x + (sizeX / grid[0]), y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)


        # fill actions
        button_rect = pygame.Rect(x + ((sizeX / grid[0])*2), y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)


        self.drawText(text=self.element["title"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=0, column=0, centered=True, right=True)
        self.drawText(text=self.element["signal"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=1, column=0, centered=True, right=True)

        info = "c: "+self.element["channel"]+", q: "+self.element["quality"]

        password = ''
        for char in self.element["txt"]:
            password += '*'
        self.drawText(text=info, x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=1, column=1, centered=True, right=True)
        self.drawText(text=password, x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=0, column=1, centered=True, right=True)

        portion = sizeY / grid[1]


    def drawText(self,text,x,y,sizeX,sizeY,grid,column,field,centered=False,right=False,font_color=COLOR_WHITE):
        if centered:
            x += ((sizeX/grid[0])/2) - ( (self.font.size(text)[0]) / 2)
        else:
            if right:
                x += (sizeX/grid[0]) - self.font.size(text)[0] - self.padding / 2
            else:
                x += self.padding / 2

        xT = x + (column * sizeX / grid[0])
        portion = sizeY / grid[1]
        yT = y + (portion*(field+1)) - (portion/2)
        yT -= (self.font.size(text)[1] / 2) #text center
        txt = self.font.render(text, True, font_color)
        self.surface.blit(txt, (xT, yT))
