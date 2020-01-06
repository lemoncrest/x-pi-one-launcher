import pygame
import os
from core.colors import *
import io
try:
    from urllib2 import urlopen # Python2
except ImportError:
    from urllib.request import urlopen # Python3 but... it's not necessary at this moment, for the furute
    pass

from core.constants import *

class SimpleMenu():

    def __init__(self,surface=None):
        self.surface = surface

    def drawNavigationBar(self,selection,total):

        up = False
        down = False

        #draw navigation flower
        flow = pygame.Rect(WINDOW_SIZE[0]-(MARGIN*2), MARGIN*2, MARGIN, (WINDOW_SIZE[1]-(MARGIN*4)))
        pygame.draw.rect(self.surface, COLOR_GRAY, flow, 0)

        #navigation up
        triangle1 = [WINDOW_SIZE[0]-(MARGIN*2), MARGIN*2]
        triangle2 = [WINDOW_SIZE[0]-(MARGIN*2)+MARGIN/2, MARGIN]
        triangle3 = [WINDOW_SIZE[0]-(MARGIN), MARGIN*2]
        color = COLOR_LIGHT_GRAY

        position = pygame.mouse.get_pos()
        #calculate color with rectangles
        if pygame.Rect(WINDOW_SIZE[0]-(MARGIN*2),MARGIN,MARGIN,MARGIN).collidepoint(position):
            color = COLOR_GREEN
            up = True

        pygame.draw.polygon(self.surface, color, [triangle1, triangle2, triangle3], 0)

        #navigation down
        triangle1 = [WINDOW_SIZE[0]-(MARGIN*2), WINDOW_SIZE[1]-MARGIN*2]
        triangle2 = [WINDOW_SIZE[0]-(MARGIN*2)+MARGIN/2, WINDOW_SIZE[1]-MARGIN]
        triangle3 = [WINDOW_SIZE[0]-(MARGIN), WINDOW_SIZE[1]-MARGIN*2]

        color = COLOR_LIGHT_GRAY
        #calculate color with rectangles
        if pygame.Rect(WINDOW_SIZE[0]-(MARGIN*2),WINDOW_SIZE[1]-MARGIN*2,MARGIN,MARGIN).collidepoint(position):
            color = COLOR_GREEN
            down = True

        pygame.draw.polygon(self.surface, color, [triangle1, triangle2, triangle3], 0)

        #now calculates where should be the indicator of up and down in navigation bar
        selection+=1
        portionY = (WINDOW_SIZE[1]-(MARGIN*4))/total
        #first point
        flowX = WINDOW_SIZE[0]-(MARGIN*2)
        flowY2 = (portionY)
        #sized (portion width and height)
        flowX2 = MARGIN
        flowY = MARGIN*2 + (portionY*(selection-1))

        flow = pygame.Rect(flowX, flowY, flowX2, flowY2)
        pygame.draw.rect(self.surface, COLOR_DARK_GRAY, flow, 0)

        return up,down

    def drawSelectedElement(self,element,path,aTxt,bTxt):
        fontSize = 30
        font = pygame.font.Font(None, fontSize)

        #draw card with transparency
        card = pygame.Surface((WINDOW_SIZE[0]-(MARGIN*2), WINDOW_SIZE[1]-(MARGIN*2)), pygame.SRCALPHA)
        color_with_alpha = COLOR_BLUE
        color_with_alpha = color_with_alpha+(128,)
        pygame.draw.rect(card, color_with_alpha, (0,0, WINDOW_SIZE[0]-(MARGIN*2),WINDOW_SIZE[1]-(MARGIN*2)))
        self.surface.blit(card,(MARGIN,MARGIN))

        title = "unknown"
        if "name" in element:
            title = element["name"]
        elif "title" in element:
            title = element["title"]

        txt = font.render(str(title), True, COLOR_GREEN)
        self.surface.blit(txt, (MARGIN*2, WINDOW_SIZE[1]-(MARGIN*2)-(fontSize*2)))

        if "launcher" in element:
            txt2 = font.render(str(element["launcher"]), True, COLOR_LIGHT_GRAY)
            self.surface.blit(txt2, (MARGIN*2, WINDOW_SIZE[1]-(MARGIN)-(fontSize*2)))

        #now draw image if exists
        if path!=None and "http" not in path:
            filename = os.path.join(path,element["source"],element["thumbnail"])
        elif "://" in element["thumbnail"]:
            filename = element["thumbnail"]
            image_str = urlopen(filename).read()
            filename = io.BytesIO(image_str) #overwrite

        picture = pygame.image.load(filename)
        pic = pygame.transform.scale(picture, (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))

        self.surface.blit(pic, (MARGIN*2, MARGIN*2))

        #button A
        circleA = (THUMBNAIL_WIDTH+MARGIN*4+BUTTON_RADIO, MARGIN*2+BUTTON_RADIO)
        pygame.draw.circle(self.surface, COLOR_GREEN, circleA, BUTTON_RADIO, 0)
        txt3 = font.render("A", True, COLOR_WHITE)
        self.surface.blit(txt3, (circleA[0]-8, circleA[1]-10))
        txt33 = font.render(aTxt, True, COLOR_WHITE)
        self.surface.blit(txt33, (circleA[0]+BUTTON_RADIO*2,circleA[1]-10))

        #button B
        circleB = (THUMBNAIL_WIDTH+MARGIN*4+BUTTON_RADIO, MARGIN*2+int(MARGIN/2)+BUTTON_RADIO*3)
        pygame.draw.circle(self.surface, COLOR_RED, circleB , BUTTON_RADIO, 0)
        txt4 = font.render("B", True, COLOR_WHITE)
        self.surface.blit(txt4, (circleB[0]-8,circleB[1]-10))
        txt4 = font.render(bTxt, True, COLOR_WHITE)
        self.surface.blit(txt4, (circleB[0]+BUTTON_RADIO*2,circleB[1]-10))

        return circleA,circleB
