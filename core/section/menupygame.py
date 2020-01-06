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
import logging

from core.constants import *

logging.basicConfig(filename=os.path.join(PATH, "log.txt"), level=logging.DEBUG)
logger = logging.getLogger(__name__)
from core.colors import *
from core.components.upbar import UpBar

from core.components.squaredmenu import SquaredMenu
from core.components.simplemenu import SimpleMenu
from core.components.downloadprogressbar import DownloadProgressBar
from core.components.dialog import Dialog
from core.components.simplenotification import SimpleNotification
from core.components.mainpygame import MainPyGame
from core.section.gogpygame import GOGPygame
from core.section.itchpygame import ItchPygame
from core.section.repositorypygame import RepositoryPygame
from core.section.settingspygame import SettingsPygame
from core.components.floatlist import FloatList

class MenuPygame(MainPyGame, SquaredMenu, SimpleMenu, DownloadProgressBar, GOGPygame, ItchPygame, RepositoryPygame, SettingsPygame):

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
        self.gog = None #TODO check if it could be serialized, stored, restored and synchronized with background process
        self.itch = None

    def main(self):
        self.notification = SimpleNotification(surface=self.surface,clock=self.clock,parent=self)
        #show notification for dev revision
        self.notification.showNotification(text='dev revision')
        options = [
            {
                "title" : "Aceptar"
            }
        ]
        #show alert for configuration
        self.dialog = Dialog(surface=self.surface,title="Welcome",message="Please configure before use",options=options)
        self.dialog.draw()

        self.drawMainMenu()

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

    #used to refresh main menu
    def drawMainMenuComponents(self,menus,selected,visibleOptions):
        # draw components
        #self.drawComponents()  # at this moment bars
        self.upbar.drawBackground()
        self.upbar.refresh()
        self.upbar.menu.draw()
        #self.upbar.drawWidgets()

        # clean events, needs to be after drawComponents
        self.changes = False

        # now draw menus
        rectangles = self.drawSquaredMenus(menus, selected, visibleOptions)

        return rectangles

    #used to get widgets updated
    def lastTimeWorker(self):
        if self.lastTime + timedelta(seconds=1) > datetime.now():
            #logger.debug("refreshing time at %s " % datetime.now())
            self.lastTime = datetime.now()
            self.upbar.drawWidgets()
            self.changes = False

    def manageMainEvents(self, menus, visibleOptions=4):  # TODO
        exit = False
        selected = 0
        self.changes = True
        #build component
        self.upbar = UpBar(surface=self.surface)

        # colored background
        self.main_background()

        refreshed = False

        self.lastTime = datetime.now()

        hiddenNotification = None

        while not exit:

            self.clock.tick(FPS)

            if self.changes:
                # clean and put background
                self.main_background()

                rectangles = self.drawMainMenuComponents(menus, selected, visibleOptions)

                # clear events
                pygame.event.clear()

            if hiddenNotification is not None:
                self.changes = True
                if hiddenNotification + timedelta(seconds=1) > datetime.now():
                    #self.notification = None
                    pass

            if (self.notification is not None and self.notification.active): #TODO
                if (self.notification is not None and self.notification.active):
                    hiddenNotification = datetime.now()
                    #logger.debug("updating when notification is shown... %s" % hiddenNotification)
            elif hiddenNotification is not None and hiddenNotification+timedelta(seconds=1) > datetime.now():
                if not refreshed:
                    self.main_background()
                    rectangles = self.drawMainMenuComponents(menus, selected, visibleOptions)
                    refreshed = True
                    logger.debug("launched one refresh of the components before wait 1 second of last notification was hidden")
            elif hiddenNotification is not None:
                logger.debug("launched final refresh of the components after 1 second of last notification was hidden")
                hiddenNotification = None
                if self.notification:
                    self.main_background()
                    rectangles = self.drawMainMenuComponents(menus, selected, visibleOptions)

            self.lastTimeWorker()

            # DEBUG: get events and configure
            events = pygame.event.get()
            if len(events) != 0:
                logger.debug("mainEvent event %s" % str(events))

            #now manage dialog
            options = None
            if self.dialog is not None and self.dialog.active:
                options = self.dialog.draw(focus=selected)
            else:
                self.dialog = None
            for event in events:
                # normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    self.changes = True
                    if event.key == pygame.K_ESCAPE:
                        if self.dialog is not None and self.dialog.active:
                            self.dialog.active = False
                            selected = 0
                        else:
                            exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.dialog is not None and self.dialog.active:
                            # normal part
                            if selected < len(options) - 1:
                                selected += 1
                        else:
                            # normal part
                            if selected < len(menus) - 1:
                                selected += 1
                    elif event.key == pygame.K_LEFT:
                        # normal part
                        if selected > 0:
                            selected -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.dialog is not None and self.dialog.active:
                            # normal part
                            if selected < len(options) - 1:
                                selected += 1
                        else:
                            # normal part
                            if selected < len(menus) - 1:
                                selected += 1
                    elif event.key == pygame.K_b:
                        if self.dialog is not None and self.dialog.active:
                            self.dialog.active = False
                            selected = 0
                        else:
                            #normal part
                            exit = True
                    elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                        if self.dialog is not None and self.dialog.active:
                            if "action" in options[selected]:
                                options[selected]["action"]()
                            self.dialog.active = False
                        else:
                            #normal part
                            menus[selected]["action"]()
                            self.changes = True
                            self.lastTime = datetime.now()
                    elif event.key == pygame.K_f:
                        if self.surface.get_flags() & pygame.FULLSCREEN:
                            pygame.display.set_mode(WINDOW_SIZE)
                        else:
                            pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
                elif event.type == pygame.JOYAXISMOTION:
                    self.changes = True
                    if event.axis == 1:  # up and down
                        if event.value > 0:
                            if selected < len(menus) - 1:
                                selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1
                    elif event.axis == 0:  # left and right
                        if event.value > 0:
                            if self.dialog is not None and self.dialog.active:
                                if selected < len(options) - 1:
                                    selected += 1
                            else:
                                # normal part
                                if selected < len(menus) - 1:
                                    selected += 1
                        elif event.value < 0:
                            if selected > 0:
                                selected -= 1

                elif event.type == pygame.JOYBUTTONDOWN:
                    if self.dialog is not None and self.dialog.active:
                        if event.button == 1:
                            if "action" in options[selected]:
                                options[selected]["action"]()
                        elif event.button == 2:
                            selected = 0
                        self.dialog.active = False
                    else:
                        # normal part
                        self.changes = True
                        if event.button == 1:  # button A - enter
                            menus[selected]["action"]()
                            self.changes = True
                            self.lastTime = datetime.now()
                        elif event.button == 2:  # button B - back
                            exit = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dialog is not None and self.dialog.active:
                        for i in range(0,len(options)):
                            option = options[i]
                            if option["rectangle"].collidepoint(event.pos):
                                selected = i
                    else:
                        #normal part
                        i = 0
                        self.changes = True
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
                    if self.dialog is not None and self.dialog.active:
                        newSelected = -1
                        for i in range(0, len(options)):
                            option = options[i]
                            if option["rectangle"].collidepoint(event.pos):
                                newSelected = i
                        if newSelected == selected:
                            if "action" in options[selected]:
                                options[selected]["action"]()
                            self.dialog.active = False
                            self.changes = True
                    else:
                        # normal part
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
                                    self.changes = True
                                    self.lastTime = datetime.now()
                            i += 1

            pygame.display.flip()

    def drawComponents(self):
        self.upbar.draw()

    def halt(self):
        pass

    def reboot(self):
        pass

    def exitAndAsk(self):
        options = [
            {
                "title": "Cerrar launcher",
                "action": quit
            }
        ]
        if os.path.exists("/usr/bin/kodi"):
            options.insert(0,{
                "title": "Kodi",
                "action": self.launchKodi
            })
        if os.path.exists("/usr/bin/emulationstation"):
            options.insert(0,{
                "title": "EmulationStation",
                "action": self.launchEmulationstation
            })
        if os.path.exists("/usr/bin/retroarch"):
            options.insert(0,{
                "title": "RetroArch",
                "action": self.launchRetroarch
            })
        #clear last menu
        self.main_background()
        floatList = FloatList(surface=self.surface, clock=self.clock, options=options)
        floatList.draw()

    def launchRetroarch(self):
        os.system("/usr/bin/retroarch &")
        # quit()

    def launchKodi(self):
        os.system("/usr/bin/kodi &")
        # quit()

    def launchEmulationstation(self):
        os.system("/usr/bin/emulationstation &")
        #quit()


    def quit(self):
        options = [
            {
                "title" : "Apagar el sistema",
                "action": self.halt
            },{
                "title" : "Reiniciar",
                "action" : self.reboot
            },{
                "title" : "Salir de la consola",
                "action" : self.exitAndAsk
            }
        ]
        floatList = FloatList(surface=self.surface,clock=self.clock,options=options)
        floatList.draw()

    def main_background(self):

        if self.on and self.file is not None:  # play background music
            self.surface.blit(self.pic, (0, 0))
        else:
            self.surface.fill(COLOR_BACKGROUND)

