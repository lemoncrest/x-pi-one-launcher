import abc

from core.colors import COLOR_WHITE

class ICard(abc.ABC):

    @abc.abstractmethod
    def displayCard(self, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=10):
        pass

    @abc.abstractmethod
    def drawText(self, text, x, y, sizeX, sizeY, grid, column, field, centered=False, right=False,font_color=COLOR_WHITE):
        pass