import pygame

from core.colors import *



class Card():

    def __init__(self,surface,padding,font):
        self.surface = surface
        self.padding = padding
        self.font = font

    def displayCard(self, element, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=10):

        grid = (5,5)

        # fill image
        button_rect = pygame.Rect(x, y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

        # fill title
        button_rect = pygame.Rect(x + (sizeX / grid[0]), y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)

        # fill status
        button_rect = pygame.Rect(x + ((sizeX / grid[0]) * 2), y, (sizeX / grid[0])*2, sizeY)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, button_rect, 0)

        # fill actions
        button_rect = pygame.Rect(x + ((sizeX / grid[0])*4), y, (sizeX / grid[0]), sizeY)
        pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 0)

        if selected_field:
            # draw background rectangle
            button_rect_background = pygame.Rect(x + selected_margin, y + selected_margin,
                                                 (sizeX / grid[0]) - selected_margin * 2,
                                                 sizeY - selected_margin * 2)
            pygame.draw.rect(self.surface, COLOR_BLUE, button_rect_background, 0)

        #text columns part
        self.drawText(text=element["title"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=0, column=1, centered=True)
        self.drawText(element["os"], x, y, sizeX, sizeY, grid, 1,1)
        self.drawText(str(element["size"]), x, y, sizeX, sizeY, grid, 1,3)
        self.drawText(element["version"], x, y, sizeX, sizeY, grid, 1,4)

        # check if is a list or not, if not is a txt field so needs a keyboard
        text = element["file"]
        xT = x + (sizeX * 2 / grid[0]) - (self.font.size(text)[0] / 2)
        yT = y + sizeY / (grid[1]*2) - (self.font.size(text)[1] / 2)
        txt = self.font.render(text, True, COLOR_WHITE)
        self.drawText(text=element["title"], x=x, y=y, sizeX=sizeX, sizeY=sizeY, grid=grid, field=2, column=0,
                      centered=True,right=True,selected_margin=selected_margin)

        #TODO return main and each clickable element to be checked in main loop with events

    def drawText(self,text,x,y,sizeX,sizeY,grid,column,field,centered=False,right=True,selected_margin=5):
        if centered:
            x += ((sizeX/grid[0])/2) - ( (self.font.size(text)[0]) / 2) #- ((selected_margin/2)*(column)) #+ (self.padding/2)
        else:
            if right:
                x += self.padding
            else:
                x += self.padding

        xT = x + (column * sizeX / grid[0])

        portion = sizeY / grid[1]
        yT = y + (portion*(field+1)) - (portion/2)
        yT -= (self.font.size(text)[1] / 2) #text center
        txt = self.font.render(text, True, COLOR_WHITE)
        self.surface.blit(txt, (xT, yT))