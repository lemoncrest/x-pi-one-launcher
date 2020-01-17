# coding=utf-8
import os
import traceback
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from core.section.menupygame import MenuPygame
from core.constants import PATH
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    try:
        pymenu = MenuPygame()
        pymenu.main()
    except Exception as ex:
        logger.error(ex)
        logger.error(traceback.format_exc())
        pass
