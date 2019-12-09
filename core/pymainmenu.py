# coding=utf-8

#python2 issues, div with float, not int
from __future__ import division
import gettext
import pygame
import json
import random
import os
import sys
import subprocess
import urllib2
import time
try:
    from urllib2 import urlopen # Python2
except ImportError:
    from urllib.request import urlopen # Python3 but... it's not necessary at this moment, for the furute

import io
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
from colors import *
from core.components.upbar import UpBar
from core.components.progressbar import ProgressBar
from core.components.listbox import ListBox

WINDOW_SIZE = (1366, 768)
COLOR_BACKGROUND = (61, 61, 202) # by default if there is no image to load will be shown it
FPS = 60.0
MENU_BACKGROUND_COLOR = (153, 153, 255) #TODO put it in a theme file
MENU_OPTION_MARGIN = 20  # Option margin (px)
MARGIN = 25
THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 300
BUTTON_RADIO = 28

REMOTE_REPOSITORY = "https://gitlab.gameboyzero.es/pygames/repository/raw/master/pool.json"

class PyMainMenu():

    def __init__(self):
        #init
        pygame.init()
        self.initJoysticks()
        self.playMusicFromSettings()
        # Create pygame screen and objects
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Menu principal')
        self.upbar = UpBar(surface=self.surface)

    def main(self):
        self.drawMainMenu()
        time.sleep(1/FPS)

    def drawMainMenu(self):
        menus = [
            {"title" : "Remote repository", "image" : "images/cloud.png", "action" : self.navigateRepository},
            {"title" : "Local", "image" : "images/hdd.png", "action" : self.createLocalRepo},
            {"title" : "Settings", "image" : "images/settings.png", "action" : self.settingsMenu},
            {"title" : "Exit", "image" : "images/exit.png", "action" : self.quit}
        ]
        self.manageMainEvents(menus)

    def manageMainEvents(self,menus): #TODO
        exit = False
        selected = 0
        while not exit:
            #colored background
            self.main_background()
            #draw components
            self.drawComponents() #at this moment bars
            #now draw menus
            self.drawMenus(menus,selected,3)
            #get events and configure
            events = pygame.event.get()
            logger.debug("drawList event %s"%str(events))
            for event in events:
                try:
                    self.keyboard.on_event(event) #keyboard library
                except:
                    logger.debug("no keyboard")
                    pass
                #normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected-=1
                    elif event.key == pygame.K_DOWN:
                        if selected < len(menus)-1:
                            selected+=1
                    elif event.key == pygame.K_LEFT:
                        if selected > 0:
                            selected-=1
                    elif event.key == pygame.K_RIGHT:
                        if selected < len(menus)-1:
                            selected+=1
                    elif event.key == pygame.K_b:
                        exit = True
                    elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                        menus[selected]["action"]()
                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 1: # up and down
                        if event.value > 0:
                            if selected > 0:
                                selected-=1
                        elif event.value <0:
                            if selected < len(menus)-1:
                                selected+=1
                    elif event.axis == 0: # left and right
                        if event.value > 0:
                            if selected > 0:
                                selected-=1
                        elif event.value <0:
                            if selected < len(menus)-1:
                                selected+=1
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: #button A - enter
                        menus[selected]["action"]()
                    elif event.button == 2: #button B - back
                        exit = True

            pygame.display.update()


    def drawMenus(self,menus,selected,visibleOptions):
        if visibleOptions>len(menus):
            visibleOptions = len(menus)
        start = 0
        if selected > int(visibleOptions/2):
            start = int(visibleOptions/2)
        if start+visibleOptions > len(menus):
            start = len(menus)-visibleOptions
        end = start+visibleOptions

        i = 0
        for index in range(start,end):
            self.drawMenu(i,menus[index],visibleOptions,selected=(index==selected))
            i+=1

    def drawMenu(self,i,menu,visibleOptions=3,selected=False,verticalCenteredText=False):
        surfaceSize = self.surface.get_size()
        margin = 50
        padding = 10
        font = pygame.font.Font(None, 28)

        #draw main square
        #calculate x (all have the same size)
        size = (surfaceSize[0]/visibleOptions)-margin*2
        #calculate y (square)
        y = ((surfaceSize[1]-size)/2)
        x = (size*(i)) + (margin*2*i) + margin

        menuRect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(self.surface, COLOR_GRAY, menuRect, 0)

        if selected:
            menuRect = pygame.Rect(x+padding, y+padding, size-padding*2, size-padding*2)
            pygame.draw.rect(self.surface, COLOR_WHITE, menuRect, 0)

        #draw image
        #filename = os.path.join(os.getcwd(),"assert",menu["image"])
        filename = os.path.join(os.getcwd(),"assert",menu["image"])
        picture = pygame.image.load(filename)
        pic = pygame.transform.scale(picture, (int(size-padding*2), int(size-padding*2)))
        self.surface.blit(pic, (x+padding, y+padding))

        #draw title
        title = menu["title"]

        xT = x + size/2 - (font.size(title)[0]/2)
        if verticalCenteredText:
            yT = y + size/2 - (font.size(title)[1]/2)
        else:
            yT = y + size - ( (font.size(title)[1]) + padding*2 )

        color = COLOR_WHITE
        if selected:
            color = COLOR_BLACK
        txt = font.render(title, True, color)
        self.surface.blit(txt, (xT, yT))


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
        file = None
        with open('config/configuration.json', 'r') as json_file:
            data = json.load(json_file)
            file = data["music-file"]
            on = data["music"]
        pygame.mixer.init()
        pygame.mixer.music.stop()
        if on and file is not None: # play background music
            self.music = pygame.mixer.music.load(os.path.join(os.getcwd(),"assert/music",file))
            pygame.mixer.music.play(-1)

    def drawComponents(self):
        self.upbar.draw()

    def main_background(self):
        on = False
        file = None
        file = None
        with open(os.path.join(os.getcwd(),'config/configuration.json'), 'r') as json_file:
            data = json.load(json_file)
            file = data["wallpaper-file"]
            on = data["wallpaper"]
        if on and file is not None: # play background music
            #now draw image if exists
            filename = os.path.join(os.getcwd(),"assert/wallpapers",file)

            picture = pygame.image.load(filename)
            pic = pygame.transform.scale(picture, WINDOW_SIZE)

            self.surface.blit(pic,(0,0))
        else:
            self.surface.fill(COLOR_BACKGROUND)


    def settingsMenu(self):

        self.main_background()

        #Sample options inspired on pokemon menu
        settings = [
            {
                "title" : "Username",
                "aid" : "Configure con un teclado virtual su nombre de usuario",
                "txt" : "Empty0001298347"
            },{
                "title" : "Velocidad del texto",
                "aid" : "Texto de ayuda que se muestra en un cuadro debajo",
                "choice" : [
                    "Lenta",
                    "Media",
                    "Rapida"
                ]
            }
        ]
        x=0
        y=0
        margin = 50
        self.listbox = ListBox(
            width=int(WINDOW_SIZE[0]),
            height=int(WINDOW_SIZE[1]),
            x=x,
            y=y,
            margin=margin,
            visibleOptions=7,
            padding=20,
            surface=self.surface,
            centered = True,
            aid = True,
            list=settings)

        self.listbox.show()


    def navigateRepository(self):
        #clear screen
        self.main_background()

        #first download metadata
        margin = 50
        self.progressbar = ProgressBar(width=WINDOW_SIZE[0]-margin,height=30,surface=self.surface,x=0, y=50,margin=margin,centeredText=True)
        repository = REMOTE_REPOSITORY
        response = urllib2.urlopen(repository)
        self.progressbar.updateProgressBar() #first frame
        self.lastFramed = 0
        content = self.chunk_read(response, report_hook=self.chunk_report)
        self.progressbar.updateProgressBar() #last frame
        print(content)
        self.main_background()
        #now show metadata content
        self.drawRemoteRepository(json.loads(content))

        #TODO show main menu when terminates and returns the control

    def drawRemoteRepository(self,content):
        self.drawList(content)

    def drawList(self,data):
        selected = 0
        exit = False

        while not exit:
            #colored background
            self.main_background()

            #get events and configure
            events = pygame.event.get()
            logger.debug("drawList event %s"%str(events))
            for event in events:
                try:
                    self.keyboard.on_event(event) #keyboard library
                except:
                    logger.debug("no keyboard")
                    pass
                #normal events
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
                    elif event.key == pygame.K_UP:
                        if selected > 0:
                            selected-=1
                    elif event.key == pygame.K_DOWN:
                        if selected < len(data["games"])-1:
                            selected+=1
                    elif event.key == pygame.K_b:
                        exit = True
                    elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                        exit = True #TODO install script
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: #button A - enter
                        exit = True #TODO install script
                    elif event.button == 2: #button B - back
                        exit = True

            #display selected element
            circleA,circleB = self.drawSelectedElement(element=data["games"][selected],path=None,aTxt="Install from repository",bTxt="Back to previous menu")
            up,down = self.drawNavigationBar(selected,len(data["games"]))
            pygame.display.update()


    def chunk_report(self, bytes_so_far, chunk_size, total_size):
        percent = float(bytes_so_far) / total_size
        progress = round(percent*100, 2)
        #print("Downloaded %d of %d bytes (%0.2f%%)" % (bytes_so_far, total_size, progress))
        #print(str(progress/100))
        if float(self.lastFramed + 0.0015) < progress/100 or progress>=100:
            self.lastFramed = self.progressbar.progress
            self.progressbar.updateProgressBar()

        #less frames, better times, it's not necessary refresh all time, CPU is gold for interpreter
        self.progressbar.progress = progress/100


    def chunk_read(self, response, chunk_size=8192, report_hook=None):
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
        bytes_so_far = 0
        total = ''
        while 1:
            chunk = response.read(chunk_size)
            total+=chunk
            bytes_so_far += len(chunk)

            if not chunk:
                break

            if report_hook:
                report_hook(bytes_so_far, chunk_size, total_size)

        return total #bytes_so_far

    def saveSettings(self):

        data = {}

        with open('config/configuration.json', 'r') as json_file:
            data = json.load(json_file)
            #TODO get all possible options and store activated option or text

        with open('config/configuration.json', 'w+') as json_file:
            json.dump(data, json_file, indent=4)

    def drawNavigationBar(self,selection,total):

        up = False
        down = False

        #draw navigation flower
        flow = pygame.Rect(WINDOW_SIZE[0]-(MARGIN*2), MARGIN*2, MARGIN, (WINDOW_SIZE[1]-(MARGIN*4)))
        pygame.draw.rect(self.surface, COLOR_GRAY, flow, 0)

        #navigation up
        triangle1 = [WINDOW_SIZE[0]-(MARGIN*2), MARGIN*2]
        triangle2 = [WINDOW_SIZE[0]-(MARGIN*2)+MARGIN/2, MARGIN]
        triangle3 = [WINDOW_SIZE[0]-(MARGIN), MARGIN*2]
        color = COLOR_LIGHT_GRAY

        position = pygame.mouse.get_pos()
        #calculate color with rectangles
        if pygame.Rect(WINDOW_SIZE[0]-(MARGIN*2),MARGIN,MARGIN,MARGIN).collidepoint(position):
            color = COLOR_GREEN
            up = True

        pygame.draw.polygon(self.surface, color, [triangle1, triangle2, triangle3], 0)

        #navigation down
        triangle1 = [WINDOW_SIZE[0]-(MARGIN*2), WINDOW_SIZE[1]-MARGIN*2]
        triangle2 = [WINDOW_SIZE[0]-(MARGIN*2)+MARGIN/2, WINDOW_SIZE[1]-MARGIN]
        triangle3 = [WINDOW_SIZE[0]-(MARGIN), WINDOW_SIZE[1]-MARGIN*2]

        color = COLOR_LIGHT_GRAY
        #calculate color with rectangles
        if pygame.Rect(WINDOW_SIZE[0]-(MARGIN*2),WINDOW_SIZE[1]-MARGIN*2,MARGIN,MARGIN).collidepoint(position):
            color = COLOR_GREEN
            down = True

        pygame.draw.polygon(self.surface, color, [triangle1, triangle2, triangle3], 0)

        #now calculates where should be the indicator of up and down in navigation bar
        selection+=1
        portionY = (WINDOW_SIZE[1]-(MARGIN*4))/total
        #first point
        flowX = WINDOW_SIZE[0]-(MARGIN*2)
        flowY2 = (portionY)
        #sized (portion width and height)
        flowX2 = MARGIN
        flowY = MARGIN*2 + (portionY*(selection-1))

        flow = pygame.Rect(flowX, flowY, flowX2, flowY2)
        pygame.draw.rect(self.surface, COLOR_DARK_GRAY, flow, 0)

        return up,down

    def manageLocalEvents(self):

        data = {}

        with open(os.path.join(os.getcwd(),'config/storage.json'), 'r') as json_file:
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
                            #TODO, kill with scape
                            cmd = ""
                            with open("/tmp/lastpid.pid") as f:
                                pid = f.read()
                                pid = int(pid)+1
                                cmd = "kill -9 %s" % str(pid)
                            proc = subprocess.Popen(cmd, shell=True)
                            logger.debug("program output: %s"%str(proc.stdout))
                            os.remove("/tmp/lastpid.pid")
                    elif e.key == pygame.K_UP:
                        if selected > 0:
                            selected-=1
                    elif e.key == pygame.K_DOWN:
                        if selected < len(data["games"])-1:
                            selected+=1
                    elif e.key == pygame.K_b:
                        exit = True
                    elif e.key == pygame.K_a or e.key == pygame.K_RETURN:
                        #first stop music
                        pygame.mixer.music.stop()
                        #next launch game
                        self.launch(path,data,selected)
                        #reload music when returns
                        self.playMusicFromSettings()
                        #quit()
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
                        selected-=1
                    elif selected < len(data["games"])-1 and down:
                        selected+=1
                    logger.debug("mDOWN: %s" % str(mouse_down))
                elif e.type == pygame.JOYBUTTONDOWN:
                    if e.button == 1: #button A - enter
                        #first stop music
                        pygame.mixer.music.stop()
                        #next launch game
                        self.launch(path,data,selected)
                        #reload music when returns
                        self.playMusicFromSettings()
                        #quit()
                    elif e.button == 2: #button B - back
                        exit = True
                elif e.type == pygame.JOYAXISMOTION:
                    if e.axis == 1: # up and down
                        #get value -1 is up and 1 is down
                        if e.value > 0:
                            if selected > 0:
                                selected-=1
                        elif e.value <0:
                            if selected < len(data["games"])-1:
                                selected+=1
                    elif e.axis == 0: # left and right
                        pass

                else:
                    logger.debug("other: %s"%str(e))

            self.main_background()

            #display selected element
            circleA,circleB = self.drawSelectedElement(data["games"][selected],path,"Enter inside program","Back to previous menu")
            up,down = self.drawNavigationBar(selected,len(data["games"]))

            pygame.display.update()

    def createLocalRepo(self):
        self.manageLocalEvents()
        #TODO next actions


    def launch(self,path,data,selected):
        #close and launch program
        path2 = os.path.join(path,data["games"][selected]["source"])
        cmd = "cd %s && %s" % (path2,data["games"][selected]["launcher"])
        #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        #(out, err) = proc.communicate()
        #proc = subprocess.Popen(cmd, shell=True)
        #logger.debug("program output: %s"%str(proc.stdout))
        #pid = int(proc.stdout)+1
        os.system(cmd)

    def drawSelectedElement(self,element,path,aTxt,bTxt):
        fontSize = 30
        font = pygame.font.Font(None, fontSize)

        #draw card with transparency
        card = pygame.Surface((WINDOW_SIZE[0]-(MARGIN*2), WINDOW_SIZE[1]-(MARGIN*2)), pygame.SRCALPHA)
        color_with_alpha = COLOR_BLUE
        color_with_alpha = color_with_alpha+(128,)
        pygame.draw.rect(card, color_with_alpha, (0,0, WINDOW_SIZE[0]-(MARGIN*2),WINDOW_SIZE[1]-(MARGIN*2)))
        self.surface.blit(card,(MARGIN,MARGIN))

        title = "unknown"
        if "name" in element:
            title = element["name"]
        elif "title" in element:
            title = element["title"]

        txt = font.render(str(title), True, COLOR_GREEN)
        self.surface.blit(txt, (MARGIN*2, WINDOW_SIZE[1]-(MARGIN*2)-(fontSize*2)))

        if "launcher" in element:
            txt2 = font.render(str(element["launcher"]), True, COLOR_LIGHT_GRAY)
            self.surface.blit(txt2, (MARGIN*2, WINDOW_SIZE[1]-(MARGIN)-(fontSize*2)))

        #now draw image if exists
        if path!=None and "http" not in path:
            filename = os.path.join(path,element["source"],element["thumbnail"])
        elif "://" in element["thumbnail"]:
            filename = element["thumbnail"]
            image_str = urlopen(filename).read()
            filename = io.BytesIO(image_str) #overwrite

        picture = pygame.image.load(filename)
        pic = pygame.transform.scale(picture, (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))

        self.surface.blit(pic, (MARGIN*2, MARGIN*2))

        #button A
        circleA = (THUMBNAIL_WIDTH+MARGIN*4+BUTTON_RADIO, MARGIN*2+BUTTON_RADIO)
        pygame.draw.circle(self.surface, COLOR_GREEN, circleA, BUTTON_RADIO, 0)
        txt3 = font.render("A", True, COLOR_WHITE)
        self.surface.blit(txt3, (circleA[0]-8, circleA[1]-10))
        txt33 = font.render(aTxt, True, COLOR_WHITE)
        self.surface.blit(txt33, (circleA[0]+BUTTON_RADIO*2,circleA[1]-10))

        #button B
        circleB = (THUMBNAIL_WIDTH+MARGIN*4+BUTTON_RADIO, MARGIN*2+int(MARGIN/2)+BUTTON_RADIO*3)
        pygame.draw.circle(self.surface, COLOR_RED, circleB , BUTTON_RADIO, 0)
        txt4 = font.render("B", True, COLOR_WHITE)
        self.surface.blit(txt4, (circleB[0]-8,circleB[1]-10))
        txt4 = font.render(bTxt, True, COLOR_WHITE)
        self.surface.blit(txt4, (circleB[0]+BUTTON_RADIO*2,circleB[1]-10))

        return circleA,circleB

    def applySettings(self):
        self.saveSettings()
        #wallpapers are reloaded when you save because background image is painted all time, but needs music configuration because it's controlled at the first execution time
        self.playMusicFromSettings()
