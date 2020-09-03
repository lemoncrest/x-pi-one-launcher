import os

import json
from core.component.boxlist import BoxList

from core.constants import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class SettingsPygame():

    def settingsMenu(self):

        self.main_background()

        # Sample options inspired on pokemon menu
        with open(os.path.join(PATH, 'config/configuration.json'), 'r') as json_file:
            settings = json.load(json_file)
        # now fills settings choices with folder files
        music = None
        musicFile = ""
        for element in settings:
            if "folder" in element:
                choices = []
                folder = element["folder"]
                for r, d, f in os.walk(os.path.join(PATH, "assert", folder)):
                    element["choices"] = f
                    # for file in f:
                    #    choices.append(file)
                    # element["choices"] = choices
            if element["id"] == "music":
                music = element["choices"][element["selected"]] == "Yes"
            elif element["id"] == "music-file":
                musicFile = element["choices"][element["selected"]]

        x = 0
        y = 0
        margin = 10
        self.listbox = BoxList(
            width=int(WINDOW_SIZE[0]),
            height=int(WINDOW_SIZE[1]),
            x=x,
            y=y,
            margin=margin,
            visibleOptions=5,
            padding=15,
            surface=self.surface,
            centered=True,
            aid=True,
            list=settings,
            parent=self,
            enabledDialog=True,
            questionTitle="Save changes",
            questionMessage="Do you want to save changes?",
            answerds=[
                {
                    "title" : "Yes"
                },
                {
                    "title" : "No"
                }
            ]
        )

        # reload settings in memory (for background)
        self.loadSettings()
        # refresh music if needed

        newSettings = self.listbox.show()
        if newSettings is not None:
            with open(os.path.join(PATH, 'config/configuration.json'), 'w') as json_file:
                json.dump(newSettings, json_file, indent=4)
            for newSetting in newSettings:
                if newSetting["id"] == "music":
                    newMusic = newSetting["choices"][newSetting["selected"]] == "Yes"
                elif newSetting["id"] == "music-file":
                    newMusicFile = newSetting["choices"][newSetting["selected"]]

            if music != newMusic or newMusicFile != musicFile:
                self.playMusicFromSettings()

        self.main_background()
