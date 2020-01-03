import pygame
import logging
import os
import json
from core.constants import PATH, WINDOW_SIZE
logging.basicConfig(filename=os.path.join(PATH, "log.txt"), level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MainPyGame():

    def initJoysticks(self):
        pygame.joystick.init()
        self.joystick = None
        self.joysticks = []

        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i).get_name())

        # By default, load the first available joystick.
        if (len(self.joysticks) > 0):
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        try:
            max_joy = max(self.joystick.get_numaxes(),
                          self.joystick.get_numbuttons(),
                          self.joystick.get_numhats())
        except:
            logger.debug("no controllers found")
            pass

    def playMusicFromSettings(self):
        on = False
        file = None
        data = []
        with open(os.path.join(PATH,'config/configuration.json'), 'r') as json_file:
            data = json.load(json_file)

        for setting in data:
            if "id" in setting and "selected" in setting and "choices" in setting:
                if setting["id"] == "music-file":
                    file = setting["choices"][setting["selected"]]
                elif setting["id"] == "music":
                    on = setting["choices"][setting["selected"]] == "Yes"
        pygame.mixer.init()
        pygame.mixer.music.stop()
        if on and file is not None:  # play background music
            music = pygame.mixer.music.load(os.path.join(PATH, "assert/music", file))
            pygame.mixer.music.play(-1)

    def loadSettings(self):
        self.on = False
        self.file = None
        with open(os.path.join(PATH, 'config/configuration.json'), 'r') as json_file:
            self.data = json.load(json_file)
        for setting in self.data:
            if "id" in setting and "selected" in setting and "choices" in setting:
                if setting["id"] == "wallpaper-file":
                    selected = setting["selected"]
                    self.file = setting["choices"][selected]
                elif setting["id"] == "wallpaper":
                    self.on = setting["choices"][setting["selected"]] == "Yes"
        if self.on and self.file is not None:  # play background music
            # now draw image if exists
            filename = os.path.join(PATH, "assert/wallpapers", self.file)

            picture = pygame.image.load(filename)
            self.pic = pygame.transform.scale(picture, WINDOW_SIZE)