from core.constants import PATH
from core.card.abstractcard import AbstractCard
from core.colors import COLOR_WHITE
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WifiCard(AbstractCard):

    def __init__(self,surface,padding,font,element,parent=None):
        self.surface = surface
        self.padding = padding
        self.font = font
        self.element = element
        self.parent = parent

    def displayCard(self, x, y, sizeX, sizeY, selected_field=False, selected_choice=0, selected_margin=10):
        pass #TODO
