# coding=utf-8

#python2 issues, div with float, not int
from __future__ import division
import gettext
import pygame
import pygameMenu
import json
import random
import os
import sys
import subprocess
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
from colors import *
from pygame_vkeyboard import *
from core.components.upbar import UpBar
from core.components.progressbar import ProgressBar

WINDOW_SIZE = (1366, 768)

COLOR_BACKGROUND = (61, 61, 202) # by default if there is no image to load will be shown it
FPS = 60.0
MENU_BACKGROUND_COLOR = (153, 153, 255) #transparency color in the main rectangle. TODO put it in a theme file
MENU_OPTION_MARGIN = 20  # Option margin (px)
MARGIN = 25
THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 300
BUTTON_RADIO = 28

ABOUT = [
    'using library version {0}'.format(pygameMenu.__version__),
    'opensource PyMenu to use opensource PyGame',
    'by: @{0} with love'.format("bit"),
    pygameMenu.locals.TEXT_NEWLINE,
    'contact: {0}'.format("bit@gameboyzero.es")
]

class PyMainMenu():

    main_menu = None
    about_menu = None
    settings_menu = None
    surface = None
    joystick = None
    joysticks = None

    progress = 0

    def __init__(self):
        #init
        pygame.init()
        self.initJoysticks()
        self.playMusicFromSettings()
        # Create pygame screen and objects
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Menu principal')

        self.upbar = UpBar(surface=self.surface)

    def start(self):
        #limit fps
        self.main_menu.set_fps(FPS)
        #main loop
        self.main_menu.mainloop()

        #next main loop (when exits from self.main_menu it returns the control to pymenu main)
        self.mainloop()

        self.main_menu.enable()
        self.main_menu.reset(1)
        #quit()
        #going back - baby
        self.start()

    def main(self):
        self.drawComponents() #at this moment bars
        # Create menus
        self.createAboutMenu()
        self.createSettingsMenu()
        self.createMainMenu() #last, instance because of
        self.start()

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
        with open('config/configuration.json', 'r') as json_file:
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

    def createAboutMenu(self):
        #about menu (sample)
        self.about_menu = pygameMenu.TextMenu(self.surface,
            bgfun=self.main_background,
            color_selected=COLOR_WHITE,
            font=pygameMenu.font.FONT_COMIC_NEUE,
            font_color=COLOR_BLACK,
            font_size_title=30,
            font_title=pygameMenu.font.FONT_8BIT,
            menu_color=MENU_BACKGROUND_COLOR,
            menu_color_title=COLOR_WHITE,
            menu_height=int(WINDOW_SIZE[1] * 0.6),
            menu_width=int(WINDOW_SIZE[0] * 0.6),
            onclose=pygameMenu.events.DISABLE_CLOSE,
            option_shadow=False,
            text_color=COLOR_BLACK,
            text_fontsize=20,
            title='About',
            window_height=WINDOW_SIZE[1],
            window_width=WINDOW_SIZE[0]
        )
        for m in ABOUT:
            self.about_menu.add_line(m)
        self.about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
        self.about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    def createMainMenu(self):
        #main menu
        self.main_menu = pygameMenu.Menu(self.surface,
            bgfun=self.main_background,
            color_selected=COLOR_BLUE,
            font=pygameMenu.font.FONT_8BIT,
            font_color=COLOR_LIGHT_GREEN,
            font_size=30,
            menu_alpha=70,
            menu_color=MENU_BACKGROUND_COLOR,
            menu_height=int(WINDOW_SIZE[1] * 0.85),
            menu_width=int(WINDOW_SIZE[0] * 0.9),
            onclose=pygameMenu.events.DISABLE_CLOSE,
            option_shadow=False,
            title='Menu principal',
            widget_alignment=pygameMenu.locals.ALIGN_LEFT,
            option_margin=MENU_OPTION_MARGIN,
            window_height=WINDOW_SIZE[1],
            window_width=WINDOW_SIZE[0]
        )
        self.main_menu.add_option('Repositorio', self.navigateRepository)
        self.main_menu.add_option('Local', self.createLocalRepo)
        self.main_menu.add_option('Tutorial', self.about_menu)
        self.main_menu.add_option('Configuracion', self.settings_menu)
        self.main_menu.add_option('Salir', pygameMenu.events.EXIT)

    def navigateRepository(self):
        #hide main menu
        self.main_menu.disable()
        self.main_menu.reset(1)

        self.progress = 0

        #clear
        self.main_background()

        self.drawComponents()

        ProgressBar(width=WINDOW_SIZE[0],height=80,surface=self.surface).progressbar()

        #show main menu
        #self.main_menu.enable()
        #self.main_menu.reset(1)

        #show slider with downloaded data
        self.drawKeyboard()

    def consumer(self,text):
        #TODO self.keyboard.disable() when press enter and use pynput to write all content stored in "text"
        logger.debug('Current text : %s' % text)

    def drawKeyboard(self):
        # Initializes and activates vkeyboard
        layout = VKeyboardLayout(VKeyboardLayout.QWERTY)
        self.keyboard = VKeyboard(self.surface, self.consumer, layout)
        self.keyboard.enable()


    def mainloop(self):
        exit = False
        while not exit:
            #colored background
            self.main_background()
            #get events and configure
            events = pygame.event.get()
            logger.debug("main loop %s"%str(events))
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
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1: #button A - enter
                        pass
                    elif event.button == 2: #button B - back
                        exit = True


    def saveSettings(self):

        data = {}

        with open('config/configuration.json', 'r') as json_file:
            data = json.load(json_file)
            for key,value in self.settings_menu.get_input_data().items():
                logger.debug("saving -> key: %s, value: %s - type %s" % (key,value,type(value)))
                if isinstance(value, str):
                    logger.debug("saving str")
                    data[key]=value
                elif isinstance(value, tuple):
                    logger.debug("saving tuple..")
                    value2 = value[0]
                    if value2 in ["On","Off"]:
                        value2 = bool(value[1])
                    data[key] = value2
                elif isinstance(value,bool):
                    logger.debug("saving bool")
                    data[key]=value
                else:
                    logger.debug("no saving nothing!")

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

    def manageEvents(self):

        data = {}

        with open('config/storage.json', 'r') as json_file:
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
                        if self.main_menu.is_disabled() and proc == None:
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

            self.drawComponents()
            #display selected element
            circleA,circleB = self.drawSelectedElement(data["games"][selected],path)
            up,down = self.drawNavigationBar(selected,len(data["games"]))

            pygame.display.update()

    def createLocalRepo(self):
        self.main_menu.disable()

        self.manageEvents()

        #show main menu when terminates and returns the control
        self.main_menu.enable()
        self.main_menu.reset(1)

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

    def drawSelectedElement(self,element,path):
        fontSize = 30
        font = pygame.font.Font(None, fontSize)

        #draw card
        #card = pygame.Rect(MARGIN, MARGIN, (WINDOW_SIZE[0]-(MARGIN*2)), (WINDOW_SIZE[1]-(MARGIN*2)))
        #pygame.draw.rect(self.surface, COLOR_BLUE, card, 0)
        #pygame.draw.rect(self.surface, pygame.Color(0,0,255,255), card, 0)

        #draw card with transparency
        card = pygame.Surface((WINDOW_SIZE[0]-(MARGIN*2), WINDOW_SIZE[1]-(MARGIN*2)), pygame.SRCALPHA)
        color_with_alpha = COLOR_BLUE
        color_with_alpha = color_with_alpha+(128,)
        pygame.draw.rect(card, color_with_alpha, (0,0, WINDOW_SIZE[0]-(MARGIN*2),WINDOW_SIZE[1]-(MARGIN*2)))
        self.surface.blit(card,(MARGIN,MARGIN))

        txt = font.render(str(element["title"]), True, COLOR_GREEN)
        self.surface.blit(txt, (MARGIN*2, WINDOW_SIZE[1]-(MARGIN*2)-(fontSize*2)))

        txt2 = font.render(str(element["launcher"]), True, COLOR_LIGHT_GRAY)
        self.surface.blit(txt2, (MARGIN*2, WINDOW_SIZE[1]-(MARGIN)-(fontSize*2)))

        #now draw image if exists
        filename = os.path.join(path,element["source"],element["thumbnail"])

        picture = pygame.image.load(filename)
        pic = pygame.transform.scale(picture, (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))

        self.surface.blit(pic, (MARGIN*2, MARGIN*2))

        #button A
        circleA = (THUMBNAIL_WIDTH+MARGIN*4+BUTTON_RADIO, MARGIN*2+BUTTON_RADIO)
        pygame.draw.circle(self.surface, COLOR_GREEN, circleA, BUTTON_RADIO, 0)
        txt3 = font.render("A", True, COLOR_WHITE)
        self.surface.blit(txt3, (circleA[0]-8, circleA[1]-10))
        txt33 = font.render("Enter inside program", True, COLOR_WHITE)
        self.surface.blit(txt33, (circleA[0]+BUTTON_RADIO*2,circleA[1]-10))

        #button B
        circleB = (THUMBNAIL_WIDTH+MARGIN*4+BUTTON_RADIO, MARGIN*2+int(MARGIN/2)+BUTTON_RADIO*3)
        pygame.draw.circle(self.surface, COLOR_RED, circleB , BUTTON_RADIO, 0)
        txt4 = font.render("B", True, COLOR_WHITE)
        self.surface.blit(txt4, (circleB[0]-8,circleB[1]-10))
        txt4 = font.render("Back to previous menu", True, COLOR_WHITE)
        self.surface.blit(txt4, (circleB[0]+BUTTON_RADIO*2,circleB[1]-10))

        return circleA,circleB


    def createSettingsMenu(self):
        self.settings_menu = pygameMenu.Menu(self.surface,
            bgfun=self.main_background,
            color_selected=COLOR_BLUE,
            font=pygameMenu.font.FONT_COMIC_NEUE,
            font_color=COLOR_BLACK,
            font_size=20,
            menu_alpha=70,
            menu_color=MENU_BACKGROUND_COLOR,
            menu_height=int(WINDOW_SIZE[1] * 0.85),
            menu_width=int(WINDOW_SIZE[0] * 0.9),
            onclose=pygameMenu.events.DISABLE_CLOSE,
            option_shadow=False,
            title='Configuraciones',
            widget_alignment=pygameMenu.locals.ALIGN_LEFT,
            option_margin=MENU_OPTION_MARGIN,
            window_height=WINDOW_SIZE[1],
            window_width=WINDOW_SIZE[0]
        )
        #load settings
        with open('config/configuration.json') as json_file:
            data = json.load(json_file)

            self.settings_menu.add_text_input(title='Name: ',textinput_id="name", default=str(data["name"]),onfocus=self.drawKeyboard)
            self.settings_menu.add_text_input(title='Surname: ',textinput_id="surname", default=str(data["surname"]))

            vals = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(os.path.join(os.getcwd(),"assert/wallpapers")):
                for file in f:
                    vals.append((file,file)) #key - value

            self.settings_menu.add_selector(
                selector_id = "wallpaper-file",
                default=0,
                title = 'Wallpapers',
                values = vals
            )

            vals2 = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(os.path.join(os.getcwd(),"assert/music")):
                for file in f:
                    vals2.append((file,file)) #key - value

            self.settings_menu.add_selector(
                selector_id = "music",
                default=0,
                title = 'Enable music',
                values = [("Off",0),("On",1)]
            )

            self.settings_menu.add_selector(
                selector_id = "music-file",
                default=0,
                title = 'Music track',
                values = vals2
            )

            self.settings_menu.add_option('Apply - Save', self.applySettings)
            self.settings_menu.add_option('Back', pygameMenu.events.BACK)

    def applySettings(self):
        self.saveSettings()
        #wallpapers are reloaded when you save because background image is painted all time, but needs music configuration because it's controlled at the first execution time
        self.playMusicFromSettings()
