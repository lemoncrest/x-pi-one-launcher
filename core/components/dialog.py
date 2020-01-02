import pygame
from core.constants import *
from core.colors import *

class Dialog():

    def __init__(self,surface,width=0,height=0,title="Dialog title",message="Dialog message",options=[],fontSize = 30):
        self.surface = surface
        self.width = width
        self.height = height
        self.padding = 10
        self.margin = 50
        self.title = title
        self.message = message
        self.font = pygame.font.Font(None, fontSize)
        #fix for big title
        if (self.font.size(self.title)[0]) > self.width:
            self.width = (self.font.size(self.title)[0])+(self.padding*2)
        #fix for big message
        if (self.font.size(self.message)[0]) > self.width:
            self.width = (self.font.size(self.message)[0])+(self.padding*2)

        #fix for too litle height
        if (self.font.size(self.title)[1] + self.margin)*3 > self.height:
            self.height = (self.font.size(self.title)[1] + self.margin)*3

        self.options = options
        self.active = False

        self.button_part = self.height/4
        self.button_height = self.button_part-(self.padding*2)

        #calculate centered rectangle
        self.x = (WINDOW_SIZE[0]-self.width)/2
        self.y = (WINDOW_SIZE[1] - self.height) / 2

    def draw(self):

        self.active = True

        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, COLOR_LIGHT_GRAY, dialog_rect, 0)

        #now title part

        title_height = (self.font.size(self.title)[1])+(self.padding*2)

        dialog_rect = pygame.Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), title_height)
        pygame.draw.rect(self.surface, COLOR_GRAY, dialog_rect, 0)

        xT = (WINDOW_SIZE[0]/2) - ((self.font.size(self.title)[0]) / 2)
        yT = self.y + (title_height/2)

        txt = self.font.render(self.title, True, COLOR_BLACK)
        self.surface.blit(txt, (xT, yT) )

        yT2 = self.y + (self.height*2/5)
        xT2 = (WINDOW_SIZE[0]/2) - ((self.font.size(self.message)[0]) / 2) #TODO, break lines

        txt2 = self.font.render(self.message, True, COLOR_BLACK)
        self.surface.blit(txt2, (xT2, yT2))

        if self.options is not None and len(self.options)>0:
            # draw each option
            i = 0
            for option in self.options:
                i+=1
                self.drawButton(message=option["title"],max=len(self.options),figure=i)
        else: #draw an ok
            self.drawButton(message="ok")


    def drawButton(self,message,max=1,figure=1):
        print((max,figure))
        button_width = self.font.size(message)[1] + (self.margin * 2)

        xT3 = ((((self.width/2) / max)) * figure * 2) + self.x - (button_width/2) - ((((self.width/2) / max)) )

        yT3 = self.y + self.height - self.button_part
        button_rect = pygame.Rect(xT3, yT3, button_width, self.button_height)
        pygame.draw.rect(self.surface, COLOR_BLACK, button_rect, 0)

        txtMessage = self.font.render(message, True, COLOR_WHITE)
        self.surface.blit(txtMessage, (xT3-(self.font.size(message)[0]/2) + (button_width/2) , yT3-(self.font.size(message)[1]/2) + self.button_height/2) )