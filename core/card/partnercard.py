import pygame

from core.colors import *
#from core.components.downloadprogressbar import DownloadProgressBar
from core.component.progressbar import ProgressBar
import os
from core.constants import PATH
from core.card.icard import ICard
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class PartnerCard(ICard):

    def __init__(self,surface,padding,font,element,parent=None):
        self.surface = surface
        self.padding = padding
        self.font = font
        self.progressbar = None
        self.element = element
        self.parent = parent

    def displayCard(self, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=10):

        grid = (5,5)

        # fill image
        button_rect = pygame.Rect(x, y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

        # fill title
        button_rect = pygame.Rect(x + (sizeX / grid[0]), y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)

        # fill status
        button_rect = pygame.Rect(x + ((sizeX / grid[0]) * 2), y, (sizeX / grid[0])*2, sizeY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

        # fill actions
        button_rect = pygame.Rect(x + ((sizeX / grid[0])*4), y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)

        if selected_field:
            # draw background rectangle
            button_rect_background = pygame.Rect(x + selected_margin, y + selected_margin,
                                                 (sizeX / grid[0]) - selected_margin * 2,
                                                 sizeY - selected_margin * 2)
            pygame.draw.rect(self.surface, COLOR_BLUE, button_rect_background, 0)

        #text columns part
        if "genre" in self.element: #gog
            self.drawText(text=self.element["genre"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=0, column=1, centered=False, right=True)
            self.drawText(text=self.element["os"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=1, column=1, centered=False, right=True)
            self.drawText(text=str(self.element["size"]), x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=4, column=1, centered=False, right=False)
            self.drawText(text=self.element["version"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=4, column=1, centered=False, right=True)

        self.drawText(text=self.element["title"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=2, column=0, centered=True, right=True)

        portion = sizeY / grid[1]
        field = 2 # 0, 1, 2...
        if self.progressbar is None:
            self.progressbar = ProgressBar(
                width=sizeX/grid[0] * 2,
                height=portion,
                surface=self.surface,
                x= x + ((sizeX / grid[0]) * 2) - self.padding,
                y= y ,
                margin=self.padding*2,
                centeredText=True,
                textMessage="Obtaining...")

        if "downloading" in self.element and self.element["downloading"] and "md5" in self.element: #gog
            if self.parent is not None and self.parent.gog.md5 == self.element["md5"]:
                self.element["progress"] = self.parent.gog.state / 100 #0 - 1
                self.element["message"] = self.parent.gog.message
            if "progress" in self.element:
                self.progressbar.progress = self.element["progress"]
                self.progressbar.textMessage = self.element["message"]
                self.progressbar.updateProgressBar(parentEvents=True)
        elif "downloading" in self.element and self.element["downloading"]: #itch
            if self.parent.itch.target == self.element["link"]:
                self.element["progress"] = self.parent.itch.state / 100  # 0 - 1
            if "progress" in self.element:
                self.progressbar.progress = self.element["progress"]
                #self.progressbar.textMessage = self.parent.itch.message
                self.progressbar.updateProgressBar(parentEvents=True)
            #logger.debug(self.parent.itch.link+"--"+self.element["link"])
                

        #TODO return main and each clickable element to be checked in main loop with events

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