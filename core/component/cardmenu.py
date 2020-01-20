# coding=utf-8
# python2 issues, div with float, not int
from __future__ import division

import pygame
from core.colors import *
from core.constants import PATH
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from core.constants import *

class CardMenu():

    def __init__(self, width, height, x, y, margin, visibleOptions, padding, surface, list, card, centered=True, parent=None, selected_margin=10, onEventEnter=None):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.margin = margin
        self.list = list
        if len(list) < visibleOptions:
            visibleOptions = len(list)
        self.visibleOptions = visibleOptions
        self.padding = padding
        self.surface = surface
        self.barWidth = 20  # TODO
        self.fontSize = 20  # TODO
        self.font = pygame.font.Font(None, self.fontSize)
        self.centered = centered
        self.parent = parent
        self.selected_margin = selected_margin
        self.onEventEnter = onEventEnter
        self.card = card


    def show(self):
        if self.visibleOptions<=0:
            return None #TODO

        # display options
        sizeX = self.width - (self.margin * 2) - (self.padding*3) - self.barWidth
        figure = self.visibleOptions
        sizeY = (self.height - (self.padding * (self.visibleOptions + 1)) - (self.margin * 2)) / figure

        exit = False

        selected = 0
        choices = []
        #will manage individual selection about a card (left and right event selection button)
        for i in range(0, len(self.list)):
            index = 0
            #TODO here the up comment, by the way, with 0 is great
            choices.append(index)

        changes = True

        while not exit:
            self.parent.clock.tick(FPS)

            #check if there is some downloading process in background
            for i in range(0, len(self.list)):
                if self.parent is not None and (self.parent.gog is not None and "md5" in self.list[i] and self.list[i]["md5"] == self.parent.gog.md5):
                    self.list[i]["downloading"] = True
                    logger.debug(self.list[i])

            if changes:
                # colored background
                self.parent.main_background()
                changes = False

            events = pygame.event.get()
            if len(events) != 0:
                logger.debug("cardmenu event %s" % str(events))

            for event in events:
                # normal events

                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                        changes = True
                    elif event.key == pygame.K_DOWN:
                        if selected < len(self.list) - 1:
                            selected += 1
                        changes = True
                    elif event.key == pygame.K_LEFT:
                        if choices[selected] > 0:
                            choices[selected] -= 1

                    elif event.key == pygame.K_RIGHT:
                        if "choices" in self.list[selected]:
                            if choices[selected] < len(self.list[selected]["choices"]) - 1:
                                choices[selected] += 1

                    elif event.key == pygame.K_RETURN:
                        #TODO put in a function, copy reference to joybuttondown and do a new function for launching installed game (feature requested)
                        if "genre" in self.list[selected]: #gog
                            target = self.list[selected]["title"]
                        elif "link" in self.list[selected]:
                            target = self.list[selected]["link"]
                        self.list[selected]["downloading"] = True
                        if self.onEventEnter is not None:
                            self.onEventEnter(target)
                        changes = True
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1:  # button A - enter
                        changes = True #TODO action
                    elif event.button == 2:  # button B - back
                        exit = True
                elif event.type == pygame.JOYAXISMOTION:
                    changes = True #TODO review
                    if event.axis == 1:  # up and down
                        if event.value > 0:
                            if selected < len(self.list) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1
                    elif event.axis == 0:  # left and right
                        if event.value > 0:
                            if "choices" in self.list[selected]:
                                if choices[selected] < len(self.list[selected]["choices"]) - 1:
                                    choices[selected] += 1
                        elif event.value < 0:
                            if choices[selected] > 0:
                                choices[selected] -= 1

            # display all options
            self.displayCards(sizeX, sizeY, selected, choices)

            # display lateral bar
            self.displayBar(sizeX, sizeY, selected)

            pygame.display.flip()  # update

        return self.list  # items updated to be saved


    def displayBar(self, sizeX, sizeY, selected):
        x = sizeX + self.x + self.margin + self.padding*2
        y = self.y + self.margin + self.padding
        sizeX = self.barWidth
        sizeY = self.height - (self.padding * 2) - (self.margin * 2)

        button_rect = pygame.Rect(x, y, sizeX, sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)

        sizeSelectedY = sizeY / len(self.list)
        button_rect = pygame.Rect(x, y + (selected * sizeSelectedY), sizeX, sizeSelectedY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

    def displayCards(self, sizeX, sizeY, selected, choices):

        first = selected - int(self.visibleOptions / 2)
        if first < 0:
            first = 0
        elif first + self.visibleOptions > len(self.list):
            first = len(self.list) - self.visibleOptions
        last = first + self.visibleOptions

        for i in range(first, last):
            if self.centered:
                x = ((WINDOW_SIZE[0]) / 2) - ((self.width - (self.margin * 2) - (self.padding*2) - self.barWidth)/2) #(sizeX / 2) + ((self.padding*2 + self.barWidth) / 2) #- ( self.margin*2 )#self.x + self.margin
            else:
                x = self.x + self.margin
            choice = choices[i]
            y = self.y + self.margin + ((i + 1 - first) * self.padding) + ((i - first) * sizeY)
            #TODO store in a list (big rectangle) to be checked in main loop for events
            card = self.card(surface=self.surface, padding=self.padding, font=self.font, element=self.list[i],parent=self.parent)
            card.displayCard(x=x, y=y, sizeX=sizeX, sizeY=sizeY,selected_field=bool(i == selected),selected_choice=0,selected_margin=self.selected_margin)
