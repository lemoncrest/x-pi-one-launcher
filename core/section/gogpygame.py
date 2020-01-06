import pygame
import os
import codecs
import json

from core.constants import *

from core.component.progressbar import ProgressBar
from core.component.cardmenu import CardMenu

from core.partner.gogrepo import AttrDict #issues related to read data with coded
from core.partner.gog import GOG

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GOGPygame():

    def navigateGOG(self):
        self.main_background()
        endDays = 90
        # check if cookies exists or is invalid dated
        cookiesFile = os.path.join(PATH, "config", GOG.COOKIES_FILENAME)
        login = not os.path.exists(cookiesFile) #TODO python3 issues related to timesstamp for next days in "endDays"
        manifestFile = os.path.join(PATH, "config", GOG.MANIFEST_FILENAME)
        update = not os.path.exists(manifestFile) #TODO
        #login = (not os.path.exists(cookiesFile)) or (os.path.getctime(cookiesFile) < (datetime.now() - timedelta(days=endDays)))
        logger.debug("login process %s" % str(login))
        if self.gog is None:
            username = ""
            password = ""
            dir = ""
            with open(os.path.join(PATH, "config", 'configuration.json'), 'r') as json_file:
                data = json.load(json_file)
                for element in data:
                    if element["id"] == 'gog_user':
                        username = element["txt"]
                    elif element["id"] == 'gog_password':
                        password = element["txt"]
                    elif element["id"] == 'gog_tmp':
                        dir = element["txt"]

            self.gog = GOG(username, password, dir)

        if login:
            self.gog.login()
            self.manageGOGLoginEvents()

        #update = (not os.path.exists(manifestFile)) or (os.path.getctime(manifestFile) < (datetime.now() - timedelta(days=endDays)))
        logger.debug("update process %s" % str(update))
        if update:
            self.gog.update()  # all your games
            self.manageGOGUpdateEvents()
            # gog.update(id='wasteland_2_kickstarter')
        #get elements from gog-manifest.dat
        elements = []
        #with open(manifestFile, 'r') as manifest:
        if os.path.exists(manifestFile):
            with codecs.open(manifestFile, 'rU', 'utf-8') as r:
                data = r.read().replace('{', 'AttrDict(**{').replace('}', '})')
                data = eval(data)
            logger.debug("ok, data loaded, now loop")
            elements = []  # holds tuples of (title, filename) with md5 as key

            for game in data:
                for game_item in game.downloads:
                    if game_item.md5 is not None:
                        element = {}
                        element["title"] = game.title
                        element["file"] = game_item.name
                        element["os"] = game_item.os_type
                        element["size"] = game_item.size
                        element["version"] = game_item.version
                        element["desc"] = game_item.desc
                        element["genre"] = game.genre
                        element["background"] = "http"+game.bg_url+".jpg"
                        element["image"] = "http"+game.image_url+".jpg"
                        element["md5"] = game_item.md5 #TODO
                        elements.append(element)

            logger.debug("ok, data obtained, now display")

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
                list=elements,
                selected_margin=10,
                parent=self,
                onEventEnter=self.gog.download
            )
            self.cardmenu.show()

            #self.gog.download()
            #self.manageGOGDownloadEvents()
        else:
            logger.debug("manifest doesn't exists")

    def manageGOGDownloadEvents(self):
        self.manageGOGEvent(errorCode=100, textMessage='Downloading...')

    def manageGOGUpdateEvents(self):
        self.manageGOGEvent(errorCode=9, textMessage='Updating...')

    def manageGOGLoginEvents(self):
        self.manageGOGEvent(errorCode=5, textMessage='Login...')

    def manageGOGEvent(self, errorCode, textMessage='Starting...'):
        exit = False
        margin = 50
        self.progressbar = ProgressBar(width=WINDOW_SIZE[0] - margin, height=30, surface=self.surface, x=0, y=50,
                                       margin=margin, centeredText=True, textMessage=textMessage)

        self.main_background()  # take into account it should be inside instead out of the while, but at this moment is a better performance

        while not exit:
            self.clock.tick(FPS)

            self.progressbar.textMessage = self.gog.message
            state = self.gog.state

            if state >= errorCode:
                exit = True
                self.progressbar.progress = 1
            else:
                self.progressbar.progress = state / errorCode
                # logger.debug(str(self.progressbar.progress))

            events = pygame.event.get()
            for event in events:
                # normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True

            self.progressbar.updateProgressBar(parentEvents=True)
            pygame.display.flip()