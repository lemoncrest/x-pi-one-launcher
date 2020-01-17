
import pygame
import os
import json

import subprocess

from core.constants import *

from core.component.progressbar import ProgressBar

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
            aid=True,
            list=networks,
            parent=self,
            enabledDialog=True,
            questionTitle="Exit",
            questionMessage="Do you want to exit from configuration?",
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