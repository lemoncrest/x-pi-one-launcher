# coding=utf-8
import pygame
import os
import subprocess
from core.colors import *
from core.components.menu import Menu
from datetime import datetime
from core.constants import *

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
        widthTime = self.drawTime()
        #next audio
        widthAudio = self.drawAudio(start=widthTime)
        #widthAudio2 = self.drawAudio(start=widthTime+widthAudio)

    def drawAudio(self,start):
        cmd = "amixer -D pulse sget Master | grep 'Left:' | awk -F'[][]' '{ print $2 }'"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        level = out.decode("utf-8")
        level = level[:len(level)-2] #remove % character
        number = False
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
            rect = pygame.Rect(x - (self.padding*2) - (self.margin*2), 0, width + (self.padding*2)+ (self.margin*2), BARSIZE)
            pygame.draw.rect(self.surface, COLOR_BLACK, rect)

            #first display speaker
            pygame.draw.polygon(self.surface,COLOR_WHITE,( (x+(top/2),y+0),(x+(top/4),y+(top/4)),(x+0,y+(top/4)),(x+0,y+(top*3/4)),(x+(top/4),y+(top*3/4)),(x+(top/2),y+top) ))
            #next display bars
            bars = int(int(level)/14)
            barSize = 2
            init = WINDOW_SIZE[0] - width - start + top / 2 + self.padding*2
            for x in range(bars):
                rect = pygame.Rect(init + self.padding*x*2, y, barSize, top)
                pygame.draw.rect(self.surface,COLOR_WHITE,rect)

        return width

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

        return width