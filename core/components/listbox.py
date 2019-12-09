# coding=utf-8

#python2 issues, div with float, not int
from __future__ import division

import pygame
from core.colors import *

from core.components.keyboard import *

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

WINDOW_SIZE = (1366, 768)

class ListBox():

    def __init__(self,width,height,x,y,margin,visibleOptions,padding,surface,list,centered=True,aid = False):
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
        self.aid = aid
        self.keyboard = VirtualKeyboard()

    def show(self):
        #TODO display navigation bar with margins
        #display options
        sizeX = self.width - (self.margin*2) - (self.padding*2) - self.barWidth
        figure = self.visibleOptions
        if self.aid:
            figure += 1
        sizeY = (self.height-(self.padding*(self.visibleOptions+1)) - (self.margin*2)) / figure

        exit = False

        selected = 0
        choices = []
        #TODO put selected index from configuration in each choices[i]
        for i in range(0,len(self.list)):
            choices.append(0)

        while not exit:

            events = pygame.event.get()
            logger.debug("drawList event %s"%str(events))

            for event in events:
                try:
                    self.keyboard.on_event(event) #keyboard library
                except:
                    logger.debug("no keyboard")
                    pass
                #normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.keyboard.state == 1:
                            self.keyboard.disable() #self.keyboard.state = 0
                        else: #no keyboard -> exit
                            exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected-=1
                    elif event.key == pygame.K_DOWN:
                        if selected < len(self.list)-1:
                            selected+=1
                    elif event.key == pygame.K_LEFT:
                        if choices[selected] > 0:
                            choices[selected]-=1
                    elif event.key == pygame.K_RIGHT:
                        if "choices" in self.list[selected] :
                            if choices[selected] < len(self.list[selected]["choices"])-1:
                                choices[selected]+=1
                    elif event.key == pygame.K_RETURN:
                        if "txt" in self.list[selected] :
                            self.keyboard.run(self.surface, self.list[selected]["choices"][self.list[selected]["selected"]])
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: #button A - enter
                        if "txt" in self.list[selected] and "visible" in self.list[selected] and self.list[selected]["visible"]:
                            self.keyboard.enable()
                    elif event.button == 2: #button B - back
                        if self.keyboard.state == 1:
                            self.keyboard.disable() #self.keyboard.state = 0
                        else: #no keyboard -> exit
                            exit = True

            if self.keyboard.state == 0:

                #display all options
                self.displayOptions(sizeX,sizeY,selected,choices)

                #display lateral bar
                self.displayBar(sizeX,sizeY,selected)

                if self.aid:
                    self.displayAid(selected,sizeX,sizeY)


            pygame.display.flip() #update

    def consumer(self,text):
        logger.debug('Current text : %s' % text)


    #TODO display description of selected element in a black box at botton of the list
    def displayAid(self,selected,sizeX,sizeY):

        if self.centered:
            x = ((WINDOW_SIZE[0])/2) - (sizeX/2)
        else:
            x = self.x

        y = self.y + self.margin + ((self.visibleOptions+1)*self.padding) + ((self.visibleOptions)*sizeY)

        button_rect = pygame.Rect(x, y, sizeX, sizeY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

        xT = x+self.padding
        yT = y+sizeY/2-(self.font.size(self.list[selected]["aid"])[1]/2)

        txt = self.font.render(self.list[selected]["aid"], True, COLOR_BLACK)
        self.surface.blit(txt, (xT, yT))


    def displayBar(self,sizeX,sizeY,selected):
        x = sizeX+self.x+self.margin+self.padding
        y = self.y + self.margin + self.padding
        sizeX = self.barWidth
        sizeY = self.height-(self.padding*2)-(self.margin*2)
        if self.aid:
            #at this moment the same space like an option
            sizeY -= (self.height-(self.padding*(self.visibleOptions+1)) - (self.margin*2)) / (self.visibleOptions+1)

        button_rect = pygame.Rect(x, y, sizeX, sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)

        sizeSelectedY = sizeY / len(self.list)
        button_rect = pygame.Rect(x, y+(selected*sizeSelectedY), sizeX, sizeSelectedY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

    def displayOptions(self,sizeX,sizeY,selected,choices):

        first = selected-int(self.visibleOptions/2)
        if first<0:
            first = 0
        elif first+self.visibleOptions>len(self.list):
            first = len(self.list)-self.visibleOptions
        last = first+self.visibleOptions

        for i in range(first,last):
            if self.centered:
                x = ((WINDOW_SIZE[0])/2) - (sizeX/2)
            else:
                x = self.x
            choice = choices[i]
            y = self.y + self.margin + ((i+1-first)*self.padding) + ((i-first)*sizeY)
            self.displayOption(element=self.list[i], x=x, y=y, sizeX=sizeX, sizeY=sizeY,selected_field=bool(i==selected),selected_choice=choice)


    def displayOption(self,element,x,y,sizeX,sizeY,selected_field=False,selected_choice=0,selected_margin=15):

        #fill title
        button_rect = pygame.Rect(x, y, (sizeX/3)-self.padding, sizeY)
        pygame.draw.rect(self.surface, COLOR_BLACK, button_rect, 0)

        if selected_field:
            #draw background rectangle
            button_rect_background = pygame.Rect(x+selected_margin, y+selected_margin, (sizeX/3)-self.padding-selected_margin*2, sizeY-selected_margin*2)
            pygame.draw.rect(self.surface, COLOR_BLUE, button_rect_background, 0)

        xT = x+self.padding
        yT = y+sizeY/2-(self.font.size(element["title"])[1]/2)
        txt = self.font.render(element["title"], True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))

        #fill options
        firstX = x+(sizeX/3)-self.padding
        lastX = (sizeX*2/3)-self.padding
        button_rect = pygame.Rect(firstX, y, lastX, sizeY)
        pygame.draw.rect(self.surface, COLOR_DARK_GRAY, button_rect, 0)

        #check if is a list or not, if not is a txt field so needs a keyboard
        if "choices" in element:
            barHeight = 20 #TODO
            left_rect = pygame.Rect(firstX+self.padding, y+self.padding, barHeight, sizeY-(self.padding*2))
            pygame.draw.rect(self.surface, COLOR_GRAY, left_rect, 0)
            right_rect = pygame.Rect(firstX+lastX-(self.padding*2), y+self.padding, barHeight, sizeY-(self.padding*2))
            pygame.draw.rect(self.surface, COLOR_GRAY, right_rect, 0)

            text = element["choices"][selected_choice]
        elif "txt" in element: #txt
            text = element["txt"]

        xT = x + (sizeX*2/3)-(self.font.size(text)[0]/2)
        yT = y+sizeY/2-(self.font.size(text)[1]/2)
        txt = self.font.render(text, True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))
