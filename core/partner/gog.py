from threading import Thread
#engine
from core.partner.gogrepo import *
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

class GOG():

    COOKIES_FILENAME = COOKIES_FILENAME
    MANIFEST_FILENAME = MANIFEST_FILENAME

    def __init__(self,user,password,downloadDir='/tmp/'):
        self.user = user
        self.password = password
        self.oslist = ["linux"]
        self.langlist = ["es","en"]
        self.targetDir = downloadDir
        self.state = 0
        self.message = "waiting..."
        self.md5 = ""

    def login(self):
        self.state = 0
        logger.info("init login launch...")
        t = Thread(target=self.login_worker)
        t.daemon = True
        t.start()
        logger.info("login launched!")

    def login_worker(self):
        cmd_login(self.user,self.password,parent=self)

    def update(self,id=None):
        self.state = 0
        logger.info("init update launch...")
        t = Thread(target=self.update_worker)
        t.daemon = True
        t.start()
        logger.info("update launched!")

    def update_worker(self,id=None):
        cmd_update(os_list=self.oslist,lang_list=self.langlist,skipknown=False,updateonly=False,id=id,parent=self)

    def download(self,targetId):
        self.targetId = targetId
        self.state = 0
        logger.info("init download launch...")
        t = Thread(target=self.download_worker)
        t.daemon = True
        t.start()
        logger.info("download launched!")

    def download_worker(self):
        #args.savedir, args.skipextras, args.skipgames, args.skipids, args.dryrun, args.id
        #savedir, skipextras, skipgames, skipids, dryrun, id
        cmd_download(savedir=self.targetDir,skipextras=True,skipgames=False,skipids=False,dryrun=False,id=self.targetId,parent=self)
