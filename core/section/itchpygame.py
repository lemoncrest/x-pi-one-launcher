import os
import json

from core.component.cardmenu import CardMenu
from core.partner.itch import Itch

import logging

from core.constants import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ItchPygame():

    def navigateItch(self):

        self.main_background()

        if self.itch is None:
            username = ""
            password = ""
            dir = ""
            with open(os.path.join(PATH, "config", 'configuration.json'), 'r') as json_file:
                data = json.load(json_file)
                for element in data:
                    if element["id"] == 'itch_user':
                        username = element["txt"]
                    elif element["id"] == 'itch_password':
                        password = element["txt"]
                    elif element["id"] == 'itch_tmp':
                        dir = element["txt"]
            self.itch = Itch(username,password, dir,self)

            self.itch.login()
            self.elements = self.itch.getGames()

        self.cardmenu = CardMenu(
            width=int(WINDOW_SIZE[0]),
            height=int(WINDOW_SIZE[1]),
            x=0,
            y=0,
            margin=25,
            visibleOptions=4,
            padding=20,
            surface=self.surface,
            centered=True,
            list=self.elements,
            selected_margin=10,
            parent=self,
            onEventEnter=self.itch.downloadGame
        )
        self.cardmenu.show()