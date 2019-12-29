import pygame
import time
from core.colors import *

try:
    from datetime import datetime
except:
    import datetime
    pass

from core.constants import *

class SimpleNotification():

    def __init__(self,surface=None,clock=None):
        self.surface = surface
        self.clock = clock
        self.x = 0
        self.y = 0
        self.fontSize = 30
        self.font = pygame.font.Font(None, self.fontSize)

    def showNotification(self,text="Default notification"):
        notificate = True
        firstDatetime = datetime.now()
        while notificate:

            width = self.font.size(text)[0] + (self.margin*2)
            height = self.font.size(text)[1] + (self.margin*2)

            notificationRect = pygame.Rect(self.x, self.y, width, height) #TODO, review

            pygame.draw.rect(self.surface, COLOR_BLACK, notificationRect, 0)

            font_color = COLOR_WHITE
            self.font.render(text, True, font_color)

            self.clock.flip(FPS)


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
