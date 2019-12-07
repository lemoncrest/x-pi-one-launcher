# coding=utf-8

#python2 issues, div with float, not int
from __future__ import division

import pygame
from core.colors import *
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

WINDOW_SIZE = (1366, 768)

class ListBox():

    def __init__(self,width,height,x,y,margin,visibleOptions,padding,surface,list,centered=True):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.margin = margin
        self.list = list
        if len(list)<visibleOptions:
            visibleOptions = len(list)
        self.visibleOptions = visibleOptions
        self.padding = padding
        self.surface = surface
        self.barWidth = 20 # TODO
        self.fontSize = 25 # TODO
        self.font = pygame.font.Font(None, self.fontSize)
        self.centered = centered

    def show(self):
        #TODO display navigation bar with margins
        #display options
        sizeX = self.width - (self.margin*2) - (self.padding*2) - self.barWidth
        sizeY = (self.height-(self.padding*(self.visibleOptions+1)) - (self.margin*2)) / self.visibleOptions

        selected = 3
        first = 0
        last = self.visibleOptions
        for i in range(first,last):
            if self.centered:
                x = ((WINDOW_SIZE[0])/2) - (sizeX/2)
            else:
                x = self.x

            y = self.y + self.margin + ((i+1)*self.padding) + ((i)*sizeY)
            self.displayOption(element=self.list[i], x=x, y=y, sizeX=sizeX, sizeY=sizeY,selected_field=bool(i==selected),selected_choice=0)

        #display lateral bar
        self.displayBar(sizeX,sizeY)

        pygame.display.flip() #update
        #display description of selected element in a black box at botton of the list


    def displayBar(self,sizeX,sizeY):
        x = sizeX+self.x+self.margin+self.padding
        y = self.y + self.margin + self.padding
        sizeX = self.barWidth
        sizeY = self.height-(self.padding*2)-(self.margin*2)
        button_rect = pygame.Rect(x, y, sizeX, sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)


    def displayOption(self,element,x,y,sizeX,sizeY,selected_field=False,selected_choice=0,selected_margin=15):

        text = element["title"]
        list = element["choice"]
        #fill title
        button_rect = pygame.Rect(x, y, (sizeX/3)-self.padding, sizeY)
        pygame.draw.rect(self.surface, COLOR_BLACK, button_rect, 0)

        if selected_field:
            #draw background rectangle
            button_rect_background = pygame.Rect(x+selected_margin, y+selected_margin, (sizeX/3)-self.padding-selected_margin*2, sizeY-selected_margin*2)
            pygame.draw.rect(self.surface, COLOR_BLUE, button_rect_background, 0)

        xT = x+self.padding
        yT = y+sizeY/2-(self.font.size(text)[1]/2)
        txt = self.font.render(text, True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))

        #fill options
        firstX = x+(sizeX/3)-self.padding
        lastX = (sizeX*2/3)-self.padding
        button_rect = pygame.Rect(firstX, y, lastX, sizeY)
        pygame.draw.rect(self.surface, COLOR_DARK_GRAY, button_rect, 0)

        barHeight = 20 #TODO
        left_rect = pygame.Rect(firstX+self.padding, y+self.padding, barHeight, sizeY-(self.padding*2))
        pygame.draw.rect(self.surface, COLOR_GRAY, left_rect, 0)
        right_rect = pygame.Rect(firstX+lastX-(self.padding*2), y+self.padding, barHeight, sizeY-(self.padding*2))
        pygame.draw.rect(self.surface, COLOR_GRAY, right_rect, 0)

        text = list[selected_choice]
        xT = x + (sizeX*2/3)-(self.font.size(text)[0]/2)
        yT = y+sizeY/2-(self.font.size(text)[1]/2)
        txt = self.font.render(text, True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))
