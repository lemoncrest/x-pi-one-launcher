import pygame
import time
from core.colors import *

try:
    from datetime import datetime, timedelta
except:
    import datetime
    pass

from core.constants import *
from core.colors import *
from threading import Thread

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class SimpleNotification():

    def __init__(self,surface,clock,up=False,right=True):
        self.surface = surface
        self.clock = clock
        self.fontSize = 30
        self.font = pygame.font.Font(None, self.fontSize)
        self.margin = 15
        self.x = 0
        self.y = 0
        self.up = up
        self.right = right

    def showNotification(self,text="Default notification", seconds=3):
        if not self.up:
            self.y = WINDOW_SIZE[1]
        if self.right:
            self.x = WINDOW_SIZE[0]
        self.seconds = seconds
        self.text = text
        t = Thread(target=self.worker)
        t.daemon = True
        t.start()


    def worker(self):
        firstDatetime = datetime.now()

        while bool(firstDatetime+timedelta(seconds=self.seconds) > datetime.now()):

            self.clock.tick(FPS)

            width = self.font.size(self.text)[0] + (self.margin*2)
            height = self.font.size(self.text)[1] + (self.margin*2)

            rect_x = self.x
            rect_y = self.y

            x = self.x + self.margin
            y = self.y + self.margin

            if not self.up:
                y -= height
                rect_y -= height
            if self.right:
                x -= width
                rect_x -= width


            notificationRect = pygame.Rect(rect_x, rect_y, width, height) #TODO, review

            pygame.draw.rect(self.surface, COLOR_BLACK, notificationRect, 0)

            txt = self.font.render(self.text, True, COLOR_WHITE)

            textPoint = (x, y)
            logger.debug(textPoint)
            self.surface.blit(txt, textPoint)

            #pygame.display.flip() #TODO check a multithread throuble
