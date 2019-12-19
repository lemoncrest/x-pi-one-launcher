import pygame
import os
from core.colors import *

PATH = '/opt/pygamemenu/'

class SquaredMenu():

    def __init__(self,surface=None):
        self.surface = surface

    def drawSquaredMenus(self, menus, selected, visibleOptions):
        if visibleOptions>len(menus):
            visibleOptions = len(menus)
        start = 0
        if selected >= int(visibleOptions/2):
            start = selected
        if start+visibleOptions > len(menus):
            start = len(menus)-visibleOptions
        end = start+visibleOptions
        i = 0
        rectangles = []
        for index in range(start,end):
            rect = self.drawSquaredMenu(i, menus[index], visibleOptions, selected=(index == selected))
            rectangles.append(rect)
            i+=1

        return rectangles

    def drawSquaredMenu(self, i, menu, visibleOptions=3, selected=False, verticalCenteredText=False):
        surfaceSize = self.surface.get_size()
        margin = 100 - (18*visibleOptions)
        padding = 10
        font = pygame.font.Font(None, 28)

        #draw main square
        #calculate x (all have the same size)
        size = (surfaceSize[0]/visibleOptions)-margin*2
        #calculate y (square)
        y = ((surfaceSize[1]-size)/2)
        x = (size*(i)) + (margin*2*i) + margin

        menuRect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(self.surface, COLOR_GRAY, menuRect, 0)

        if selected:
            menuRect = pygame.Rect(x+padding, y+padding, size-padding*2, size-padding*2)
            pygame.draw.rect(self.surface, COLOR_WHITE, menuRect, 0)

        #draw image
        #filename = os.path.join(PATH,"assert",menu["image"])
        filename = os.path.join(PATH,"assert",menu["image"])
        picture = pygame.image.load(filename)
        pic = pygame.transform.scale(picture, (int(size-padding*2), int(size-padding*2)))
        self.surface.blit(pic, (x+padding, y+padding))

        #draw title
        title = menu["title"]

        xT = x + size/2 - (font.size(title)[0]/2)
        if verticalCenteredText:
            yT = y + size/2 - (font.size(title)[1]/2)
        else:
            yT = y + size - ( (font.size(title)[1]) + padding*2 )

        color = COLOR_WHITE
        if selected:
            color = COLOR_BLACK
        txt = font.render(title, True, color)
        self.surface.blit(txt, (xT, yT))

        return menuRect