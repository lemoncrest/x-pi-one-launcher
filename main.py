# coding=utf-8

import pygame
import pygameMenu

import random

#import os
#os.environ['SDL_VIDEO_CENTERED'] = '1'

COLOR_BACKGROUND = (61, 61, 202)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_LIGHT_GREEN = (10, 200, 10)
COLOR_LIGHT_GRAY = (120, 120, 120)
COLOR_GRAY = (30, 30, 30)

FPS = 60.0
MENU_BACKGROUND_COLOR = (153, 153, 255)
WINDOW_SIZE = (1024, 600)
MENU_OPTION_MARGIN = 45  # Option margin (px)

ABOUT = [
    'using library version {0}'.format(pygameMenu.__version__),
    'by: @{0} with love'.format("bit"),
    pygameMenu.locals.TEXT_NEWLINE,
    'contact: {0}'.format("bit@gameboyzero.es")
]

class PyMenu():


    clock = None
    main_menu = None
    about_menu = None
    surface = None

    def main_background(self):
        self.surface.fill(COLOR_BACKGROUND)

    def main(self):

        #init
        pygame.init()

        # Create pygame screen and objects
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Menu principal')
        self.clock = pygame.time.Clock()

        # Create menus

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

        self.main_menu.add_option('Repositorio', self.progressbar)
        self.main_menu.add_option('Tutorial', self.about_menu)
        self.main_menu.add_option('Configuracion', self.about_menu)
        self.main_menu.add_option('Salir', pygameMenu.events.EXIT)

        #limit fps
        self.main_menu.set_fps(FPS)

        #main loop
        while True:

            #it's just fps limitation
            self.clock.tick(FPS)

            #colored background
            self.main_background()

            #events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main menu
            self.main_menu.mainloop(events, disable_loop=False)

            # Flip surface
            pygame.display.flip()

    def progressbar(self):
        #hide main menu
        self.main_menu.disable()
        self.main_menu.reset(1)

        time = random.random()

        while time<=1.002:

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

            self.clock.tick(FPS)

            time+=0.002

            # Application events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE and self.main_menu.is_disabled():
                        self.main_menu.enable()
                        # Quit this function, then skip to loop of main-menu on line 317
                        return

            #pass events to mainmenu (previous menu)
            self.main_menu.mainloop(events)

            pygame.display.flip()

        exit()


if __name__ == '__main__':
    pymenu = PyMenu()
    pymenu.main()