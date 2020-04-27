import pygame

import json
import os

from core.constants import *

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from core.component.downloadprogressbar import DownloadProgressBar
from core.component.simplemenu import SimpleMenu

class RepositoryPygame(SimpleMenu,DownloadProgressBar):

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
        pixelateTime = None

        while not exit:
            # colored background
            self.main_background()

            if not pixelateTime:
                pixelate(self.surface,False)
                pixelateTime = True

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
