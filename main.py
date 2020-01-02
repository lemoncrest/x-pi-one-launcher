# coding=utf-8
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from core.pymainmenu import PyMainMenu

if __name__ == '__main__':
    pymenu = PyMainMenu()
    pymenu.main()
