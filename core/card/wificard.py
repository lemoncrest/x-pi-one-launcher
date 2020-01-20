from core.constants import PATH
from core.card.icard import ICard
from core.colors import COLOR_WHITE
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WifiCard(ICard):

    def displayCard(self, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=10):
        pass #TODO

    def drawText(self, text, x, y, sizeX, sizeY, grid, column, field, centered=False, right=False,font_color=COLOR_WHITE):
        pass #TODO