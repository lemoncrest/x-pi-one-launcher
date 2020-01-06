# coding=utf-8

#python2 issues, div with float, not int
from __future__ import division

import pygame
from core.colors import *
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class ProgressBar():

    def __init__(self, x, y, width, height, surface, margin=0, fontSize=20, border=2, centeredText = True ,progress = 0,color_progress=True,textMessage = "Downloading..."):
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
        self.progress = progress
        self.color_progress = color_progress
        self.textMessage = textMessage

    def updateProgressBar(self,parentEvents=False):

        #print("OK (%.2f%%)" % self.progress)

        #self.progress = progress

        exit = False
        #while progress<=1.002 and not exit:

        pygame.draw.rect(self.surface, COLOR_BLACK, self.button_rect, 0) #fill background
        color_text = COLOR_GRAY
        if not self.color_progress:
            #calculate progress color background bar
            color = COLOR_LIGHT_GRAY
            if self.progress<=0.25:
                color = COLOR_RED
            elif self.progress<=0.5:
                color = COLOR_LIGHT_GRAY
            elif self.progress<=0.75:
                color = COLOR_BLUE
            elif self.progress<1:
                color = COLOR_GREEN
            else:
                color = COLOR_WHITE
        else:
            color = (255-int(255*self.progress),int(255*self.progress),0)
            color_text = (int(255*self.progress),255-int(255*self.progress),128)

        width = (self.width-self.margin-self.border) * self.progress
        height = self.height-self.border
        pygame.draw.rect(self.surface, color, (self.x+self.margin+(self.border/2), self.y+self.margin+(self.border/2), width, height))

        progress = str(self.progress*100)
        progress = progress[0:progress.find(".") + 3]
        text = "%s %s %%" % (self.textMessage,progress)
        txt = self.font.render(text, True, color_text)

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

        exit = parentEvents #exit is not used, no while or for
        if not parentEvents:
            exit = self.manageEvents()


    def manageEvents(self):
        exit = False
        # Application events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and self.main_menu.is_disabled():
                    exit = True
        return exit

    def updateProgress(self):
        #simulate downloading... TODO download real metadata
        return self.progress
