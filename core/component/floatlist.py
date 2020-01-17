import pygame
from core.constants import *
from core.colors import *

import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class FloatList():

    def __init__(self,surface,clock,options,margin=25,padding=25):
        self.surface = surface
        self.clock = clock
        self.options = options
        self.changes = True
        self.margin = margin
        self.padding = padding
        self.font = pygame.font.Font(None, 30)
        self.maxX = 0
        self.focusMargin = 5
        self.focus_color = COLOR_BLUE
        self.background_option_color = COLOR_LIGHT_GRAY
        self.font_color = COLOR_BLACK
        self.background_alpha = COLOR_BLACK + (ALPHA,)
        self.background = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.SRCALPHA)

    def draw(self):

        exit = False
        selected = 0
        rectangles = None
        pygame.draw.rect(self.background, self.background_alpha, (0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]))
        self.surface.blit(self.background, (0, 0))
        while not exit:
            self.clock.tick(FPS)

            if self.changes:
                self.drawMainRectangle()
                rectangles = self.drawOptions(selected)

            events = pygame.event.get()
            for event in events:
                #exit = True #TODO put events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # normal part
                    i = 0
                    for rectangle in rectangles:
                        if rectangle.collidepoint(event.pos):
                            logger.debug("I will launch and select position %s" % i)
                            self.options[selected]["action"]()
                            exit = True
                        i += 1
                elif event.type == pygame.JOYBUTTONDOWN:
                    # normal part
                    self.changes = True
                    if event.button == 1:  # button A - execute
                        self.options[selected]["action"]()
                        exit = True
                    elif event.button == 2:  # button B - back
                        exit = True
                elif event.type == pygame.JOYAXISMOTION:
                    self.changes = True
                    if event.axis == 1:  # up and down
                        if event.value > 0:
                            if selected < len(self.options) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1
                    elif event.axis == 0:  # left and right
                        if event.value > 0:
                            # normal part
                            if selected < len(self.options) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    elif event.key == pygame.K_DOWN:
                        if selected < len(self.options) - 1:
                            selected += 1
                    elif event.key == pygame.K_ESCAPE:
                        exit = True
                    elif event.key == pygame.K_RETURN:
                        if "action" in self.options[selected]:
                            self.options[selected]["action"]()
                        exit = True

            pygame.display.flip()


    def drawMainRectangle(self):
        if self.maxX == 0:
            self.maxX = 0
            self.maxY = 0
            #first needs calculate what is the maximum size of all rectangles
            for option in self.options:
                sizeX = self.font.size(option["title"])[0]+ (self.padding*2)
                if sizeX>self.maxX:
                    self.maxX = sizeX
                sizeY = self.font.size(option["title"])[1] + (self.padding * 2)
                if sizeY>self.maxY:
                    self.maxY = sizeY

            #now using max. sizes calculate the background total size
            self.sizeX = self.maxX + self.margin*2
            self.sizeY = (self.maxY * len(self.options)) + (self.margin * 2 * len(self.options))

            self.x = (WINDOW_SIZE[0] - self.sizeX) / 2
            self.y = (WINDOW_SIZE[1] - self.sizeY) / 2

        background_rect = pygame.Rect(self.x, self.y, self.sizeX, self.sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, background_rect, 0)

    def drawOptions(self,focus=0):
        rectangles = []
        for i in range(len(self.options)):
            option = self.options[i]
            rectangle = self.drawOption(option,i,focus==i)
            rectangles.append(rectangle)

        return rectangles

    def drawOption(self,option,i,focus=False):
        total = len(self.options)
        #background rectangle
        x = self.x+self.margin
        y = self.y+((self.margin*2*i)+self.margin) + (self.maxY*i)
        button_rect = pygame.Rect(x, y, self.maxX, self.maxY)
        pygame.draw.rect(self.surface, self.background_option_color, button_rect, 0)

        #focus rectangle
        if focus:
            button_rect = pygame.Rect(x+self.focusMargin, y+self.focusMargin, self.maxX-(self.focusMargin*2), self.maxY-(self.focusMargin*2))
            pygame.draw.rect(self.surface, self.focus_color, button_rect, 0)

        #text
        txt = self.font.render(option["title"], True, self.font_color)
        xT = (WINDOW_SIZE[0]-self.font.size(option["title"])[0]) / 2
        yT = y + ((self.maxY - self.font.size(option["title"])[1]) / 2)
        self.surface.blit(txt, (xT, yT))
        #return current button to be manage in mouse events
        return button_rect
