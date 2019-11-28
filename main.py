# coding=utf-8
#python2 issues, div with float, not int
from __future__ import division

import pygame
import pygameMenu
import json
import random
import os
import sys
import subprocess

COLOR_BACKGROUND = (61, 61, 202)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_LIGHT_GREEN = (10, 200, 10)
COLOR_LIGHT_GRAY = (150, 150, 150)
COLOR_DARK_GRAY = (60, 60, 60)
COLOR_GRAY = (90, 90, 90)

FPS = 60.0
MENU_BACKGROUND_COLOR = (153, 153, 255)
WINDOW_SIZE = (1024, 600)
MENU_OPTION_MARGIN = 45  # Option margin (px)

ABOUT = [
    'using library version {0}'.format(pygameMenu.__version__),
    'opensource PyMenu to use opensource PyGame',
    'by: @{0} with love'.format("bit"),
    pygameMenu.locals.TEXT_NEWLINE,
    'contact: {0}'.format("bit@gameboyzero.es")
]

class PyMenu():

    main_menu = None
    about_menu = None
    settings_menu = None
    surface = None

    def __init__(self):
        #init
        pygame.init()

        # Create pygame screen and objects
        #self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Menu principal')

    def main(self):
        # Create menus
        self.createAboutMenu()
        self.createSettingsMenu()
        self.createMainMenu() #last, instance because of

        # mainloop
        self.mainloop()

    def main_background(self):
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

        self.main_menu.add_option('Repositorio local', self.createLocalRepo)
        self.main_menu.add_option('Tutorial', self.about_menu)
        self.main_menu.add_option('Configuracion', self.settings_menu)
        self.main_menu.add_option('Salir', pygameMenu.events.EXIT)

    def mainloop(self):
        #limit fps
        self.main_menu.set_fps(FPS)
        #main loop
        exit = False
        self.main_menu.mainloop()
        while not exit:
            #colored background
            self.main_background()
            #get events and configure
            events = pygame.event.get()
            print(str(events))
            for event in events:
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.main_menu.is_enabled():
                        exit = True
            # Main menu
            self.main_menu.mainloop(events, disable_loop=False)
            # Flip surface
            pygame.display.update()
        exit()

    def saveSettings(self):

        data = {}

        with open('config/configuration.json', 'r') as json_file:
            data = json.load(json_file)
            for key,value in self.settings_menu.get_input_data().items():
                print("saving -> key: %s, value: %s" % (key,value))
                data[key]=value

        with open('config/configuration.json', 'w+') as json_file:
            json.dump(data, json_file, indent=4)

    def drawNavigationBar(self,selection,total):
        margin = 50

        #draw navigation flower
        flow = pygame.Rect(WINDOW_SIZE[0]-(margin*2), margin*2, margin, (WINDOW_SIZE[1]-(margin*4)))
        pygame.draw.rect(self.surface, COLOR_GRAY, flow, 0)

        #navigation right
        triangle1 = [WINDOW_SIZE[0]-(margin*2), margin*2]
        triangle2 = [WINDOW_SIZE[0]-(margin*2)+margin/2, margin]
        triangle3 = [WINDOW_SIZE[0]-(margin), margin*2]
        pygame.draw.polygon(self.surface, COLOR_LIGHT_GRAY, [triangle1, triangle2, triangle3], 0)

        #navigation right
        triangle1 = [WINDOW_SIZE[0]-(margin*2), WINDOW_SIZE[1]-margin*2]
        triangle2 = [WINDOW_SIZE[0]-(margin*2)+margin/2, WINDOW_SIZE[1]-margin]
        triangle3 = [WINDOW_SIZE[0]-(margin), WINDOW_SIZE[1]-margin*2]
        pygame.draw.polygon(self.surface, COLOR_LIGHT_GRAY, [triangle1, triangle2, triangle3], 0)

        #now calculates where should be the indicator of up and down in navigation bar
        selection+=1
        portionY = (WINDOW_SIZE[1]-(margin*4))/total
        #first point
        flowX = WINDOW_SIZE[0]-(margin*2)
        flowY2 = (portionY)
        #sized (portion width and height)
        flowX2 = margin
        flowY = margin*2 + (portionY*(selection-1))

        flow = pygame.Rect(flowX, flowY, flowX2, flowY2)
        pygame.draw.rect(self.surface, COLOR_DARK_GRAY, flow, 0)

    def createLocalRepo(self):
        self.main_menu.disable()

        data = {}

        with open('config/storage.json', 'r') as json_file:
            data = json.load(json_file)

        path = data["repo"]["path"]
        exit = False
        selected = 0
        proc = None
        while not exit:
            self.main_background()
            #display selected element
            self.drawSelectedElement(data["games"][selected],path)
            self.drawNavigationBar(selected,len(data["games"]))
            pid = 0
            # menu events
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    exit()
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
                            print("program output: %s"%str(proc.stdout))
                            os.remove("/tmp/lastpid.pid")
                    elif e.key == pygame.K_UP:
                        if selected > 0:
                            selected-=1
                    elif e.key == pygame.K_DOWN:
                        if selected < len(data["games"])-1:
                            selected+=1
                    elif e.key == pygame.K_RETURN:
                        #close and launch program
                        path2 = os.path.join(path,data["games"][selected]["source"])
                        cmd = "cd %s && %s" % (path2,data["games"][selected]["launcher"])
                        #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                        #(out, err) = proc.communicate()
                        #proc = subprocess.Popen(cmd, shell=True)
                        #print("program output: %s"%str(proc.stdout))
                        #pid = int(proc.stdout)+1
                        os.system(cmd)
                        exit()
                else:
                    print(str(e))
            pygame.display.update()

        #show main menu
        self.main_menu.enable()
        self.main_menu.reset(1)

    def drawSelectedElement(self,element,path):
        fontSize = 36
        margin = 50
        #draw card
        card = pygame.Rect(margin, margin, (WINDOW_SIZE[0]-(margin*2)), (WINDOW_SIZE[1]-(margin*2)))
        font = pygame.font.Font(None, fontSize)
        pygame.draw.rect(self.surface, COLOR_BLUE, card, 0)

        txt = font.render(str(element["title"]), True, COLOR_GREEN)
        self.surface.blit(txt, (margin*2, WINDOW_SIZE[1]-(margin*2)-(fontSize*2)))

        txt2 = font.render(str(element["launcher"]), True, COLOR_LIGHT_GRAY)
        self.surface.blit(txt2, (margin*2, WINDOW_SIZE[1]-(margin)-(fontSize*2)))

        #now draw image if exists
        filename = os.path.join(path,element["source"],element["thumbnail"])

        picture = pygame.image.load(filename)
        pic = pygame.transform.scale(picture, (300, 300))

        self.surface.blit(pic, (margin*2, margin*2))


    def load_game(self,**kwargs):
        #print("path %s launcher %s "% (path,launcher))
        print(str(kwargs))
        print(str(self.local_repo))
        for key, value in kwargs.items():
            print ("%s == %s" %(key, value))


    def createSettingsMenu(self):
        self.settings_menu = pygameMenu.Menu(self.surface,
            bgfun=self.main_background,
            color_selected=COLOR_BLUE,
            font=pygameMenu.font.FONT_COMIC_NEUE,
            font_color=COLOR_BLACK,
            font_size=30,
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

            self.settings_menu.add_text_input(title='Name: ',textinput_id="name", default=str(data["name"]))
            self.settings_menu.add_text_input(title='Surname: ',textinput_id="surname", default=str(data["surname"]))
            self.settings_menu.add_option('Save changes', self.saveSettings)
            self.settings_menu.add_option('Back', pygameMenu.events.BACK)

    def progressbar(self):
        #hide main menu
        self.main_menu.disable()
        self.main_menu.reset(1)

        time = random.random()

        exit = False

        while time<=1.002 and not exit:
            self.main_background()

            button_rect = pygame.Rect(50, 100, (WINDOW_SIZE[0]-(50*2)), 80)
            width = (WINDOW_SIZE[0]-100)*time
            FONT = pygame.font.Font(None, 36)

            pygame.draw.rect(self.surface, COLOR_GRAY, button_rect, 2)
            color = COLOR_LIGHT_GRAY
            if time<=0.25:
                color = COLOR_RED
            elif time<=0.5:
                color = COLOR_LIGHT_GRAY
            elif time<=0.75:
                color = COLOR_BLUE
            elif time<1:
                color = COLOR_GREEN
            else:
                color = COLOR_WHITE

            pygame.draw.rect(self.surface, color, (51, 100, width-1, 80))

            txt = FONT.render(str(round(time, 2)), True, color)
            self.surface.blit(txt, (20, 20))

            time+=0.002

            # Application events
            events = pygame.event.get()
            print(str(events))
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE and self.main_menu.is_disabled():
                        exit = True

            pygame.display.flip()

        #show main menu
        self.main_menu.enable()
        self.main_menu.reset(1)


if __name__ == '__main__':
    pymenu = PyMenu()
    pymenu.main()
