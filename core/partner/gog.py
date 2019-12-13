from threading import Thread

from core.partner.gogrepo import *

class GOG():

    COOKIES_FILENAME = COOKIES_FILENAME
    MANIFEST_FILENAME = MANIFEST_FILENAME

    def __init__(self,user,password):
        self.user = user
        self.password = password
        self.oslist = ["linux"]
        self.langlist = ["es","en"]
        self.targetDir = "/tmp/"

    def login(self):
        cmd_login(self.user,self.password)

    def update(self,id=None):
        cmd_update(os_list=self.oslist,lang_list=self.langlist,skipknown=False,updateonly=False,id=id)

    def download(self):
        print("download process...")
        t = Thread(target=self.download_worker)
        t.daemon = True
        t.start()
        print("download done!")

    def download_worker(self):
        #args.savedir, args.skipextras, args.skipgames, args.skipids, args.dryrun, args.id
        #savedir, skipextras, skipgames, skipids, dryrun, id
        cmd_download(savedir=self.targetDir,skipextras=True,skipgames=False,skipids=False,dryrun=False,id='wasteland_2_kickstarter')
