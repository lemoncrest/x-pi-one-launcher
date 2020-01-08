# coding=utf-8
import pygame
import os
import subprocess
from core.colors import *
from core.component.menu import Menu
from datetime import datetime
from core.constants import *

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class UpBar():

    def __init__(self,surface):
        self.surface = surface # main screen
        self.bar = pygame.Surface((WINDOW_SIZE[0], BARSIZE), pygame.SRCALPHA)
        self.bar.set_alpha(ALPHA)
        self.font = pygame.font.Font(os.path.join(PATH,"assert/fonts","DejaVuSans.ttf"), FONT_SIZE)
        self.menu = Menu(title="Menu", first=(0,0) ,parent=(WINDOW_SIZE[0],BARSIZE), font=self.font, surface=self.surface)
        self.margin = 5
        self.padding = 2

    def draw(self):
        self.drawBackground()

        self.drawWidgets()
        self.refresh()

        self.menu.draw()


    def drawBackground(self):
        # add alpha to tuple {transform (,,,) to (,,,,ALPHA)}
        black_with_alpha = COLOR_BLACK + (ALPHA, )
        pygame.draw.rect(self.bar, black_with_alpha, (0,0, WINDOW_SIZE[0],BARSIZE))

    def refresh(self):
        self.surface.blit(self.bar, (0, 0))

    def drawWidgets(self):
        #first time
        timeRect = self.drawTime()
        #next audio
        audioRect = self.drawAudio(start=timeRect.width)
        #next wifi
        wifiRect = self.drawWifi(start=(timeRect.width+audioRect.width))

    def drawWifi(self,start,totalBars=10,barWidth=3):
        cmd = "awk 'NR==3 {print $4}''' /proc/net/wireless"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        level = out.decode("utf-8").replace(".","")
        try:
            level = 2*(int(level)+80) #dBm conversion to percentage
        except:
            level = 0 #no signal
            pass

        barHeight = barWidth * 8
        width = (self.padding*2*totalBars) + (barWidth*totalBars) + (self.margin*2)
        #background
        x = WINDOW_SIZE[0] - start - width
        rect = pygame.Rect(x, 0, width, BARSIZE)
        pygame.draw.rect(self.surface, COLOR_BLACK, rect)

        #bars
        if level==0: #when no signal them display red X
            yP = int((BARSIZE - barHeight)/2)
            txt = self.font.render("X", True, COLOR_RED)
            textPoint = (x + (self.padding * (totalBars+1)  + (barWidth*totalBars/2)), yP)
            self.surface.blit(txt, textPoint)
        bars = int(level*totalBars/100)
        for i in range(0,bars,1):
            xP = x + self.padding * (i+1) * 2 + (barWidth*i) + self.margin
            ySize = int(barHeight / totalBars * i)
            yP = barHeight - ySize + BARSIZE/4#(barHeight)-(int((BARSIZE - barHeight)/2) + (barHeight/totalBars*i))

            rect = pygame.Rect(xP, yP, barWidth, ySize)
            pygame.draw.rect(self.surface, COLOR_GREEN, rect)
        for i in range(bars,totalBars,1):  # points
            txt = self.font.render(".", True, COLOR_WHITE)
            xP = x + self.padding * (i+1) * 2 + (barWidth*i) + self.margin
            yP = (BARSIZE - barHeight) - (self.font.size(".")[1] / 2)
            textPoint = (xP, yP)
            self.surface.blit(txt, textPoint)
        return rect



    def drawAudio(self,start,number=False):
        cmd = "amixer -D pulse sget Master | grep 'Left:' | awk -F'[][]' '{ print $2 }'"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        level = out.decode("utf-8")
        level = level[:len(level)-2] #remove % character
        rect = None
        if number:
            width = self.font.size("100")[0] + (self.margin * 2) #max sized to be used in background
            height = self.font.size(level)[1] + (self.margin * 2)
            x = WINDOW_SIZE[0] - width - start
            rect = pygame.Rect(x, 0, width, BARSIZE)
            pygame.draw.rect(self.surface,COLOR_BLACK,rect)
            #self.surface.blit(self.bar, rect)
            #pygame.display.update(rect)
            txt = self.font.render(level, True, COLOR_WHITE)
            x = WINDOW_SIZE[0] - start
            y = height / 2
            textPoint = (x -self.margin*3 -self.padding*3 - (self.font.size(level)[0])/2, y)
            self.surface.blit(txt, textPoint)
        else:
            top = 20
            width = top*2 + (self.margin*2) + (self.padding*2)
            height = top
            x = WINDOW_SIZE[0] - width - start
            y = (BARSIZE - height) / 2
            rect = pygame.Rect(x  - (self.margin*2), 0, width  + (self.margin*2), BARSIZE)
            pygame.draw.rect(self.surface, COLOR_BLACK, rect)

            #first display speaker
            pygame.draw.polygon(self.surface,COLOR_WHITE,( (x+(top/2),y+0),(x+(top/4),y+(top/4)),(x+0,y+(top/4)),(x+0,y+(top*3/4)),(x+(top/4),y+(top*3/4)),(x+(top/2),y+top) ))
            #next display bars
            try:
                bars = int(int(level)/14)
            except:
                bars = 0
                pass

            try:
                level = int(level)
            except:
                logger.debug("couldn't parse level '%s'" % level)
                pass
            barSize = 2
            init = WINDOW_SIZE[0] - width - start + top / 2 + self.padding*2
            if bars > 0:
                for x in range(bars):
                    rect2 = pygame.Rect(init + self.padding*x*2, y, barSize, top)
                    pygame.draw.rect(self.surface,COLOR_WHITE,rect2)
            if int(level)==0:
                txt = self.font.render("X", True, COLOR_RED)
                textPoint = (init + self.padding*2, y)
                self.surface.blit(txt, textPoint)
            else:
                #put points in the base of the bars
                for x in range(bars,int(100/14)): #7
                    txt = self.font.render(".", True, COLOR_WHITE)
                    xP = init + self.padding * x * 2
                    textPoint = (xP, (height / 2) + (self.font.size(".")[1]/2) )
                    self.surface.blit(txt, textPoint)

            #width = top*2 + (self.margin*2) + (self.padding*2)

        return rect

    def drawTime(self):

        text = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        width = self.font.size(text)[0] + (self.margin * 2)
        height = self.font.size(text)[1] + (self.margin * 2)

        #white_with_alpha = COLOR_WHITE + (ALPHA,)
        #rect = pygame.draw.rect(self.bar, white_with_alpha, (WINDOW_SIZE[0]-width, 0, width, BARSIZE))

        rect = pygame.Rect(WINDOW_SIZE[0]-width, 0, width, BARSIZE)
        #self.surface.blit(self.bar, rect)
        pygame.draw.rect(self.surface, COLOR_BLACK, rect)

        txt = self.font.render(text, True, COLOR_WHITE)

        x = WINDOW_SIZE[0]-width+self.margin
        y = height / 2
        textPoint = (x, y)
        self.surface.blit(txt, textPoint)

        #pygame.display.update(pygame.Rect(WINDOW_SIZE[0]-width, 0, width, BARSIZE))

        return rect