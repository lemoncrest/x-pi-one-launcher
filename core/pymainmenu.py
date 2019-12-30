# coding=utf-8

# python2 issues, div with float, not int
from __future__ import division
import gettext
import pygame
import json
import random
import os
import codecs
import sys
import subprocess
import time
try:
    from datetime import datetime, timedelta
except:
    import datetime
from core.partner.gogrepo import AttrDict #issues related to read data with coded
import logging

from core.constants import *

logging.basicConfig(filename=os.path.join(PATH, "log.txt"), level=logging.DEBUG)
logger = logging.getLogger(__name__)
from core.colors import *
from core.components.upbar import UpBar
from core.components.progressbar import ProgressBar
from core.components.boxlist import BoxList
from core.components.squaredmenu import SquaredMenu
from core.components.simplemenu import SimpleMenu
from core.components.downloadprogressbar import DownloadProgressBar
from core.components.cardmenu import CardMenu
from core.partner.gog import GOG
from core.partner.itch import Itch

from core.components.simplenotification import SimpleNotification


class PyMainMenu(SquaredMenu, SimpleMenu, DownloadProgressBar):

    def __init__(self):
        # init
        # pygame.init()
        pygame.display.init()
        pygame.font.init()

        self.initJoysticks()
        self.loadSettings()
        self.playMusicFromSettings()
        # Create pygame screen and objects
        self.surface = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
        #self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Menu principal')
        self.upbar = UpBar(surface=self.surface)
        self.gog = None #TODO check if it could be serialized, stored, restored and synchronized with background process
        self.itch = None

    def main(self):
        notification = SimpleNotification(surface=self.surface,clock=self.clock)
        notification.showNotification(text='Welcome')
        self.drawMainMenu()

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

    def drawMainMenu(self):
        menus = [
            {"title": "Itch.io (alpha)", "image": "images/itch.png", "action": self.navigateItch},
            {"title": "GOG (alpha)", "image": "images/GOG.png", "action": self.navigateGOG},
            {"title": "Remote repository", "image": "images/cloud.png", "action": self.navigateRepository},
            {"title": "Local", "image": "images/hdd.png", "action": self.createLocalRepo},
            {"title": "Settings", "image": "images/settings.png", "action": self.settingsMenu},
            {"title": "Exit", "image": "images/exit.png", "action": self.quit}
        ]
        self.manageMainEvents(menus)

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

    def manageMainEvents(self, menus, visibleOptions=4):  # TODO
        exit = False
        selected = 0
        changes = True
        lastTime = datetime.now()
        while not exit:
            self.clock.tick(FPS)
            if changes:
                # colored background
                self.main_background()
                # now draw menus
                rectangles = self.drawSquaredMenus(menus, selected, visibleOptions)

                # draw components
                self.drawComponents()  # at this moment bars

                lastTime = datetime.now()

                # clean events, needs to be after drawComponents
                changes = False

            if lastTime+timedelta(seconds=1) > datetime.now():
                lastTime = datetime.now()
                self.upbar.drawTime()
                # draw components
                #self.drawComponents()  # at this moment bars

            # get events and configure
            events = pygame.event.get()
            if len(events) != 0:
                logger.debug("mainEvent event %s" % str(events))
            for event in events:
                # normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    changes = True
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    elif event.key == pygame.K_DOWN:
                        if selected < len(menus) - 1:
                            selected += 1
                    elif event.key == pygame.K_LEFT:
                        if selected > 0:
                            selected -= 1
                    elif event.key == pygame.K_RIGHT:
                        if selected < len(menus) - 1:
                            selected += 1
                    elif event.key == pygame.K_b:
                        exit = True
                    elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                        menus[selected]["action"]()
                    elif event.key == pygame.K_f:
                        if self.surface.get_flags() & pygame.FULLSCREEN:
                            pygame.display.set_mode(WINDOW_SIZE)
                        else:
                            pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
                elif event.type == pygame.JOYAXISMOTION:
                    changes = True
                    if event.axis == 1:  # up and down
                        if event.value > 0:
                            if selected < len(menus) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1
                    elif event.axis == 0:  # left and right
                        if event.value > 0:
                            if selected < len(menus) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1

                elif event.type == pygame.JOYBUTTONDOWN:
                    changes = True
                    if event.button == 1:  # button A - enter
                        menus[selected]["action"]()
                    elif event.button == 2:  # button B - back
                        exit = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    i = 0
                    changes = True
                    for rectangle in rectangles:
                        if rectangle.collidepoint(event.pos):
                            if visibleOptions > len(menus):
                                visibleOptions = len(menus)
                            start = 0
                            if selected > int(visibleOptions / 2):
                                start = int(visibleOptions / 2)
                            if start + visibleOptions > len(menus):
                                start = len(menus) - visibleOptions
                            end = start + visibleOptions
                            logger.debug("start %s end %s" % (start, end))
                            logger.debug("I deduced position %s" % (start + i))
                            selected = (start + i)
                        i += 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    i = 0
                    for rectangle in rectangles:
                        if rectangle.collidepoint(event.pos):
                            if visibleOptions > len(menus):
                                visibleOptions = len(menus)
                            start = 0
                            if selected > int(visibleOptions / 2):
                                start = int(visibleOptions / 2)
                            if start + visibleOptions > len(menus):
                                start = len(menus) - visibleOptions
                            end = start + visibleOptions
                            logger.debug("start %s end %s" % (start, end))
                            logger.debug("I will launch and select position %s" % (start + i))
                            launch = selected == (start + i)
                            selected = (start + i)
                            if launch:
                                menus[selected]["action"]()
                        i += 1

            pygame.display.flip()

    def quit(self):
        logger.debug("Bye bye!")
        quit()

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
            self.music = pygame.mixer.music.load(os.path.join(PATH, "assert/music", file))
            pygame.mixer.music.play(-1)

    def drawComponents(self):
        self.upbar.draw()

    def main_background(self):

        if self.on and self.file is not None:  # play background music
            self.surface.blit(self.pic, (0, 0))
        else:
            self.surface.fill(COLOR_BACKGROUND)

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
        margin = 50
        self.listbox = BoxList(
            width=int(WINDOW_SIZE[0]),
            height=int(WINDOW_SIZE[1]),
            x=x,
            y=y,
            margin=margin,
            visibleOptions=7,
            padding=15,
            surface=self.surface,
            centered=True,
            aid=True,
            list=settings,
            parent=self
        )

        # reload settings in memory (for background)
        self.loadSettings()
        # refresh music if needed

        newSettings = self.listbox.show()
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

    def navigateRepository(self):
        # clear screen
        self.main_background()

        # first download metadata
        content = self.downloadProgressBar(remote=REMOTE_REPOSITORY)

        self.main_background()
        # now show metadata content
        self.drawRemoteRepository(json.loads(content))
        # TODO show main menu when terminates and returns the control

    def drawRemoteRepository(self, content):
        self.drawList(content)

    def drawList(self, data):
        selected = 0
        exit = False

        while not exit:
            # colored background
            self.main_background()

            # get events and configure
            events = pygame.event.get()
            if events != 0:
                logger.debug("drawList event %s" % str(events))
            for event in events:
                # normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    elif event.key == pygame.K_DOWN:
                        if selected < len(data["games"]) - 1:
                            selected += 1
                    elif event.key == pygame.K_b:
                        exit = True
                    elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                        exit = True  # TODO install script
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1:  # button A - enter
                        exit = True  # TODO install script
                    elif event.button == 2:  # button B - back
                        exit = True
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 1:  # up and down
                        # get value -1 is up and 1 is down
                        if event.value > 0:
                            if selected < len(data["games"]) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1
                    elif event.axis == 0:  # left and right
                        pass

            # display selected element
            circleA, circleB = self.drawSelectedElement(element=data["games"][selected], path=None,
                                                        aTxt="Install from repository", bTxt="Back to previous menu")
            up, down = self.drawNavigationBar(selected, len(data["games"]))
            pygame.display.flip()

    def manageLocalEvents(self):

        data = {}

        with open(os.path.join(PATH, 'config/storage.json'), 'r') as json_file:
            data = json.load(json_file)

        path = data["repo"]["path"]
        exit = False
        selected = 0
        proc = None
        up = False
        down = False
        circleA = None
        circleB = None
        while not exit:

            pid = 0
            # menu events
            events = pygame.event.get()
            mouse_pos = None
            mouse_up = False
            mouse_down = False
            for e in events:
                if e.type == pygame.QUIT:
                    quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        if proc == None:
                            exit = True
                        else:
                            # TODO, kill with scape
                            cmd = ""
                            with open("/tmp/lastpid.pid") as f:
                                pid = f.read()
                                pid = int(pid) + 1
                                cmd = "kill -9 %s" % str(pid)
                            proc = subprocess.Popen(cmd, shell=True)
                            logger.debug("program output: %s" % str(proc.stdout))
                            os.remove("/tmp/lastpid.pid")
                    elif e.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    elif e.key == pygame.K_DOWN:
                        if selected < len(data["games"]) - 1:
                            selected += 1
                    elif e.key == pygame.K_b:
                        exit = True
                    elif e.key == pygame.K_a or e.key == pygame.K_RETURN:
                        # first stop music
                        pygame.mixer.music.stop()
                        # next launch game
                        self.launch(path, data, selected)
                        # reload music when returns
                        self.playMusicFromSettings()
                        # quit()
                elif e.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = e.pos
                    mouse_up = True
                    mouse_down = False
                    logger.debug("mUP: %s" % str(mouse_down))
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = e.pos
                    mouse_up = False
                    mouse_down = True
                    if selected > 0 and up:
                        selected -= 1
                    elif selected < len(data["games"]) - 1 and down:
                        selected += 1
                    logger.debug("mDOWN: %s" % str(mouse_down))
                elif e.type == pygame.JOYBUTTONDOWN:
                    if e.button == 1:  # button A - enter
                        # first stop music
                        pygame.mixer.music.stop()
                        # next launch game
                        self.launch(path, data, selected)
                        # reload music when returns
                        self.playMusicFromSettings()
                        # quit()
                    elif e.button == 2:  # button B - back
                        exit = True
                elif e.type == pygame.JOYAXISMOTION:
                    if e.axis == 1:  # up and down
                        # get value -1 is up and 1 is down
                        if e.value > 0:
                            if selected < len(data["games"]) - 1:
                                selected += 1
                        elif e.value < 0:
                            if selected > 0:
                                selected -= 1

                    elif e.axis == 0:  # left and right
                        pass

                else:
                    logger.debug("other: %s" % str(e))

            self.main_background()

            # display selected element
            circleA, circleB = self.drawSelectedElement(data["games"][selected], path, "Enter inside program",
                                                        "Back to previous menu")
            up, down = self.drawNavigationBar(selected, len(data["games"]))

            pygame.display.flip()

    def createLocalRepo(self):
        self.manageLocalEvents()
        # TODO next actions

    def launch(self, path, data, selected):
        # close and launch program
        path2 = os.path.join(path, data["games"][selected]["source"])
        cmd = "cd %s && %s" % (path2, data["games"][selected]["launcher"])
        # proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # (out, err) = proc.communicate()
        # proc = subprocess.Popen(cmd, shell=True)
        # logger.debug("program output: %s"%str(proc.stdout))
        # pid = int(proc.stdout)+1
        os.system(cmd)
