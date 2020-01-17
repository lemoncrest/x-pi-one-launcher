
import pygame
import os
import json

import subprocess

from core.constants import *

from core.component.progressbar import ProgressBar
from core.component.dialog import Dialog
from core.component.boxlist import BoxList

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(PATH, "log.txt"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class WifiConfigurationPygame():

    def configWifi(self):

        networks = []

        #cmd = "awk 'NR==3 {print $1}''' /proc/net/wireless" # needs a out.replace(":","")
        cmd = "cat /proc/net/wireless | perl -ne '/(\w+):/ && print $1'"

        #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        #(out, err) = proc.communicate()
        #interface = out.decode("utf-8")

        #fill with network list
        #cmd = 'iwlist wlan0 scan | grep ESSID'
        cmd = "for i in $(ls /sys/class/net/ | egrep -v ^lo$); do sudo iw dev $i scan | grep SSID | awk '{print substr($0, index($0,$2)) }'; done 2>/dev/null | sort -u"

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

        (out, err) = p.communicate()

        p_status = p.wait() # This makes the wait possible

        lists = out.decode("utf-8")

        logger.debug(lists)

        for list in lists.split("\n"):
            if "SSID:" not in list and "SSID List" not in list:
                list = list.replace("\\x00","")
                element = {}
                element["title"] = list
                element["txt"] = list #TODO put the real stored password
                element["password"] = True
                if len(list)>0:
                    networks.append(element)
                logger.debug(list)

        x = int(WINDOW_SIZE[0]) - 100
        y = 50

        margin = 0

        self.listbox = BoxList(
            width=int(WINDOW_SIZE[0])-200,
            height=int(WINDOW_SIZE[1])-100,
            x=x,
            y=y,
            margin=margin,
            visibleOptions=8,
            padding=15,
            surface=self.surface,
            centered=True,
            aid=False,
            list=networks,
            parent=self,
            enabledDialog=True,
            questionTitle="Exit",
            questionMessage="Do you want to exit and save new configuration?",
            answerds=[
                {
                    "title": "Yes"
                },
                {
                    "title": "No"
                }
            ]
        )

        newList = self.listbox.show()

        if newList is None:
            dialog = Dialog(surface=self.surface, title="No network availables", message="No networks availables was detected", options=[{ "title": "Ok"}])
            dialogSelected = -1
            exit = False
            options = dialog.draw()
            while not exit:

                self.clock.tick(FPS) #review but parent always has a clock

                events = pygame.event.get()

                for event in events:
                    if event.type == pygame.QUIT:
                        exit = True
                    elif event.type == pygame.KEYDOWN:
                        exit = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if options is not None:
                            if dialog is not None and dialog.active:
                                for i in range(0, len(options)):
                                    option = options[i]
                                    if option["rectangle"].collidepoint(event.pos):
                                        dialogSelected = i
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if options is not None:
                            if dialog is not None and dialog.active:
                                newSelected = -1
                                for i in range(0, len(options)):
                                    option = options[i]
                                    if option["rectangle"].collidepoint(event.pos):
                                        newSelected = i
                                if newSelected == dialogSelected:
                                    dialog.active = False
                                    exit = True

                options = dialog.draw()

                pygame.display.flip()  # update
