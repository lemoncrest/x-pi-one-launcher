from core.colors import *
import pygame

class Utils():

    @staticmethod
    def drawRectangleButton(text,font,surface,parentSize=(0,0),margin=0,padding=0,fillWidth=False,fillHeight=False,centeredX = False,centeredY = False):

        rectangleX = margin
        rectangleY = margin
        width = parentSize[0]+padding*2-margin*2
        height = parentSize[1]+padding*2-margin*2

        #calculate
        if not fillWidth and parentSize[0]>0:
            width = font.size(text)[0]+(font.size(text[0])[0])-(padding*2)-(margin*2)
        if not fillHeight and parentSize[1]>0:
            height = font.size(text)[1]+(font.size(text[0])[1])-(padding*2)-(margin*2)

        x = width/2-(font.size(text)[0]/2)
        y = height/2-(font.size(text)[1]/2)

        if centeredX:
            rectangleX = abs((parentSize[0] - width) / 2)
            x+=rectangleX
        else:
            x+=margin
        if centeredY:
            rectangleY = abs((parentSize[1] - height) / 2)
            y+=rectangleY
        else:
            y+=margin

        print("init: %s %s" % (rectangleX,rectangleY))
        print("size: %s %s" % (width,height))
        button = pygame.Rect(rectangleX, rectangleY, width, height)
        pygame.draw.rect(surface, COLOR_GRAY, button, 0)

        txt = font.render(text, True, COLOR_WHITE)
        surface.blit(txt, (x, y) )
        return button
