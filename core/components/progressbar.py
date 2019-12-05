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

    def __init__(self, width, height, surface, margin=0, fontSize=32, border=2 ):
        self.height = height
        self.margin = margin
        self.x = margin
        self.y = margin*2
        self.total = width
        self.width = self.total - margin*2
        self.height = height
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(None, fontSize)
        self.border = border
        self.surface = surface

    def progressbar(self,progress=0):

        self.progress = progress

        exit = False
        while progress<=1.002 and not exit:
            #draw bar
            pygame.draw.rect(self.surface, COLOR_GRAY, self.button_rect, self.border)
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

            self.width = (self.total - self.x) * progress
            pygame.draw.rect(self.surface, color, (self.x+1, self.y, self.width, self.height))

            txt = self.font.render("Downloading... %s %%"%str(round(progress, 2)*100), True, color)
            self.surface.blit(txt, (self.x, self.y+(self.margin*2)))

            progress = self.updateProgress()

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
        self.progress += 0.01
        return self.progress
