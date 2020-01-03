import pygame
from core.constants import *
from core.colors import *

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

    def draw(self):

        exit = False
        selected = 0
        rectangles = None
        while not exit:
            self.clock.tick(FPS)

            if self.changes:
                self.drawMainRectangle()
                rectangles = self.drawOptions()

            events = pygame.event.get()
            for event in events:
                exit = True #TODO put events

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

    def drawOptions(self):
        rectangles = []
        for i in range(len(self.options)):
            option = self.options[i]
            rectangle = self.drawOption(option,i)
            rectangles.append(rectangle)

        return rectangles

    def drawOption(self,option,i):
        total = len(self.options)
        #background rectangle
        x = self.x+self.margin
        y = self.y+((self.margin*2*i)+self.margin) + (self.maxY*i)
        button_rect = pygame.Rect(x, y, self.maxX, self.maxY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)
        #text
        txt = self.font.render(option["title"], True, COLOR_BLACK)
        xT = (WINDOW_SIZE[0]-self.font.size(option["title"])[0]) / 2
        yT = y + ((self.maxY - self.font.size(option["title"])[1]) / 2)
        self.surface.blit(txt, (xT, yT))
        #return current button to be manage in mouse events
        return button_rect
