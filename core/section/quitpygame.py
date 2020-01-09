import os

from core.component.floatlist import FloatList

class QuitPygame():

    def halt(self):
        os.system("sudo shutdown -h now")

    def reboot(self):
        os.system("sudo reboot")

    def exitAndAsk(self):
        options = [
            {
                "title": "Cerrar launcher",
                "action": quit
            }
        ]
        if os.path.exists("/usr/bin/kodi"):
            options.insert(0,{
                "title": "Kodi",
                "action": self.launchKodi
            })
        if os.path.exists("/usr/bin/emulationstation"):
            options.insert(0,{
                "title": "EmulationStation",
                "action": self.launchEmulationstation
            })
        if os.path.exists("/usr/bin/retroarch"):
            options.insert(0,{
                "title": "RetroArch",
                "action": self.launchRetroarch
            })
        #clear last menu
        self.main_background()
        floatList = FloatList(surface=self.surface, clock=self.clock, options=options)
        floatList.draw()

    def launchRetroarch(self):
        os.system("/usr/bin/retroarch &")
        # quit()

    def launchKodi(self):
        os.system("/usr/bin/kodi &")
        # quit()

    def launchEmulationstation(self):
        os.system("/usr/bin/emulationstation &")
        #quit()


    def quit(self):
        options = [
            {
                "title" : "Apagar el sistema",
                "action": self.halt
            },{
                "title" : "Reiniciar",
                "action" : self.reboot
            },{
                "title" : "Salir de la consola",
                "action" : self.exitAndAsk
            }
        ]
        floatList = FloatList(surface=self.surface,clock=self.clock,options=options)
        floatList.draw()