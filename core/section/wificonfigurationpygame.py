
import pygame
import os
import json

from core.constants import *

from core.component.progressbar import ProgressBar

from core.component.boxlist import BoxList

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WifiConfigurationPygame():

    def configWifi(self):

        networks = []

        #fill with network list


        x = int(WINDOW_SIZE[0]) - 100
        y = 100

        margin = 0

        self.listbox = BoxList(
            width=int(WINDOW_SIZE[0])-200,
            height=int(WINDOW_SIZE[1])-200,
            x=x,
            y=y,
            margin=margin,
            visibleOptions=8,
            padding=15,
            surface=self.surface,
            centered=True,
            aid=True,
            list=networks,
            parent=self,
            enabledDialog=True,
            questionTitle="Exit",
            questionMessage="Do you want to exit from configuration?",
            answerds=[
                {
                    "title": "Yes"
                },
                {
                    "title": "No"
                }
            ]
        )

        newList = self.listbox.show()