# coding=utf-8

import pygame
import pygameMenu

#import os
#os.environ['SDL_VIDEO_CENTERED'] = '1'

COLOR_BACKGROUND = (61, 61, 202)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (10, 200, 10)
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
            font_color=COLOR_GREEN,
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

        self.main_menu.add_option('Repositorio', self.about_menu)
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


if __name__ == '__main__':
    pymenu = PyMenu()
    pymenu.main()
