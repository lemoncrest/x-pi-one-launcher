import pygame
from core.colors import *
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class ProgressBar():

    button_rect = None
    width = None
    height = None
    font = None
    progress = None
    txt = None

    def __init__(self, x, y, width, height, surface, margin=0, fontSize=20, border=2, centeredText = True ):
        self.centeredText = centeredText
        self.height = height
        self.margin = margin
        self.x = x+border
        self.y = y+border
        self.width = width
        self.height = height
        self.button_rect = pygame.Rect(self.x+self.margin, self.y+self.margin, self.width-self.margin, self.height)
        self.font = pygame.font.Font(None, fontSize)
        self.border = border
        self.surface = surface

    def progressbar(self,progress=0):

        self.progress = progress

        exit = False
        while progress<=1.002 and not exit:

            pygame.draw.rect(self.surface, COLOR_BLACK, self.button_rect, 0) #fill background

            #calculate progress color background bar
            color = COLOR_LIGHT_GRAY
            if progress<=0.25:
                color = COLOR_RED
            elif progress<=0.5:
                color = COLOR_LIGHT_GRAY
            elif progress<=0.75:
                color = COLOR_BLUE
            elif progress<1:
                color = COLOR_GREEN
            else:
                color = COLOR_WHITE

            width = (self.width-self.margin-self.border) * progress
            height = self.height-self.border
            pygame.draw.rect(self.surface, color, (self.x+self.margin+(self.border/2), self.y+self.margin+(self.border/2), width, height))

            text = "Downloading... %s %%"%str(round(progress, 2)*100)
            txt = self.font.render(text, True, COLOR_GRAY)

            if self.centeredText:
                x = self.width/2-(self.font.size(text)[0]/2)
                y = height/2-(self.font.size(text)[1]/2)
                self.surface.blit(txt, (self.x+self.margin+x, self.y+self.margin+y))
            else:
                x = self.x+(width/2)-(self.font.size(text)[0]/2)+(self.margin/2)
                y = self.y+height/2-(self.font.size(text)[1]/2)
                self.surface.blit(txt, (x, self.margin+y))

            progress = self.updateProgress()

            #draw bar
            pygame.draw.rect(self.surface, COLOR_GRAY, self.button_rect, self.border)

            exit = self.manageEvents()

            pygame.display.flip()

    def manageEvents(self):
        exit = False
        # Application events
        events = pygame.event.get()
        logger.debug("event %s"%str(events))
        for e in events:
            if e.type == pygame.QUIT:
                exit = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and self.main_menu.is_disabled():
                    exit = True
        return exit

    def updateProgress(self):
        #simulate downloading... TODO download real metadata
        self.progress += 0.001
        return self.progress
