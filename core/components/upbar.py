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
        width = self.drawTime()
        #next audio
        width = self.drawAudio(start=width)

    def drawAudio(self,start):
        cmd = "amixer -D pulse sget Master | grep 'Left:' | awk -F'[][]' '{ print $2 }'"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        level = out.decode("utf-8")
        level = level[:len(level)-2] #remove % character
        width = self.font.size(level)[0] + (self.margin * 2)
        height = self.font.size(level)[1] + (self.margin * 2)
        rect = pygame.Rect(WINDOW_SIZE[0] - width - start, 0, width, height)
        self.surface.blit(self.bar, rect)
        txt = self.font.render(level, True, COLOR_WHITE)
        x = WINDOW_SIZE[0] - width - start + self.margin
        y = height / 2
        textPoint = (x, y)
        self.surface.blit(txt, textPoint)

        #os.system(cmd)

    def drawTime(self):

        text = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        width = self.font.size(text)[0] + (self.margin * 2)
        height = self.font.size(text)[1] + (self.margin * 2)

        #white_with_alpha = COLOR_WHITE + (ALPHA,)
        #rect = pygame.draw.rect(self.bar, white_with_alpha, (WINDOW_SIZE[0]-width, 0, width, BARSIZE))

        rect = pygame.Rect(WINDOW_SIZE[0]-width, 0, width, height)
        self.surface.blit(self.bar, rect)

        txt = self.font.render(text, True, COLOR_WHITE)

        x = WINDOW_SIZE[0]-width+self.margin
        y = height / 2
        textPoint = (x, y)
        self.surface.blit(txt, textPoint)

        #pygame.display.update(pygame.Rect(WINDOW_SIZE[0]-width, 0, width, BARSIZE))

        return width