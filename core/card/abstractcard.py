import abc

from core.colors import COLOR_WHITE

class AbstractCard():

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def displayCard(self, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=10):
        pass

#    @abc.abstractmethod
    def drawText(self,text,x,y,sizeX,sizeY,grid,column,field,centered=False,right=False,font_color=COLOR_WHITE):
        if centered:
            x += ((sizeX/grid[0])/2) - ( (self.font.size(text)[0]) / 2)
        else:
            if right:
                x += (sizeX/grid[0]) - self.font.size(text)[0] - self.padding / 2
            else:
                x += self.padding / 2

        xT = x + (column * sizeX / grid[0])

        portion = sizeY / grid[1]
        yT = y + (portion*(field+1)) - (portion/2)
        yT -= (self.font.size(text)[1] / 2) #text center
        txt = self.font.render(text, True, font_color)
        self.surface.blit(txt, (xT, yT))