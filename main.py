# coding=utf-8
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from core.section.menupygame import MenuPygame

if __name__ == '__main__':
    pymenu = MenuPygame()
    pymenu.main()
