import pygame

from core.colors import *



class Card():

    def __init__(self,surface,padding,font):
        self.surface = surface
        self.padding = padding
        self.font = font

    def displayCard(self, element, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=15):

        # fill title
        button_rect = pygame.Rect(x, y, (sizeX / 3) - self.padding, sizeY)
        pygame.draw.rect(self.surface, COLOR_BLACK, button_rect, 0)

        if selected_field:
            # draw background rectangle
            button_rect_background = pygame.Rect(x + selected_margin, y + selected_margin,
                                                 (sizeX / 3) - self.padding - selected_margin * 2,
                                                 sizeY - selected_margin * 2)
            pygame.draw.rect(self.surface, COLOR_BLUE, button_rect_background, 0)

        xT = x + self.padding
        yT = y + sizeY / 2 - (self.font.size(element["title"])[1] / 2)
        txt = self.font.render(element["title"], True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))

        # fill options
        firstX = x + (sizeX / 3) - self.padding
        lastX = (sizeX * 2 / 3) - self.padding
        button_rect = pygame.Rect(firstX, y, lastX, sizeY)
        pygame.draw.rect(self.surface, COLOR_DARK_GRAY, button_rect, 0)

        # check if is a list or not, if not is a txt field so needs a keyboard
        text = element["size"]

        xT = x + (sizeX * 2 / 3) - (self.font.size(text)[0] / 2)
        yT = y + sizeY / 2 - (self.font.size(text)[1] / 2)
        txt = self.font.render(text, True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))

        #TODO return main and each clickable element to be checked in main loop with events