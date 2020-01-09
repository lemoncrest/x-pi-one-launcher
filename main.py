# coding=utf-8
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from core.section.menupygame import MenuPygame
from core.constants import PATH
import logging
logging.basicConfig(filename=os.path.join(PATH, "log.txt"))
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        pymenu = MenuPygame()
        pymenu.main()
    except Exception as ex:
        logger.error(ex)
        pass
