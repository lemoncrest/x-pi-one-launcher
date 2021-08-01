from threading import Thread
import urllib
import requests
#engine
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

try:
    import http.cookiejar
except:
    import cookielib
    pass

class GOG():

    LOGIN_URL = 'https://login.gog.com/login'
    LOGIN_CHECK_URL = 'https://login.gog.com/login_check'

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
        user = self.user
        password = self.password
        parent=self

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://itch.io',
            'Referer': GOG.LOGIN_URL
        }

        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        urllib.request.install_opener(opener)

        response = urllib.request.urlopen(url=GOG.LOGIN_URL)

        #from response read login[_token]
        #<input type="hidden" id="login__token" name="login[_token]" value="????????" />
        html = response.read().decode("utf-8")
        token = html[html.find('<input type="hidden" id="login__token" name="login[_token]" value="')+len('<input type="hidden" id="login__token" name="login[_token]" value="'):]
        token = token[:token.find('"')]

        print("TOKEN: %s" % token)

        form = {
            'login[username]' : user,
            'login[password]' : password,
            'login[login_flow]' : 'default',
            'login[_token]' : token
        }

        cookies = ''

        for key,value in response.info().items():
            if key.lower() == 'set-cookie':
                #cookie = value
                cookie = (value[0:value.find(" Path=/;")]+" ")
                if 'Expires=' in cookie:
                    cookie = cookie[0:cookie.find('Expires=')]
                cookies+= cookie


        headers = {}
        headers["Cookie"] = cookies
        print(".."+headers["Cookie"]+"..")

        data = urllib.parse.urlencode(form).encode('utf-8')

        response = urllib.request.urlopen(url=GOG.LOGIN_CHECK_URL,data=data)

        html2 = response.read().decode('utf-8')
        if 'Change password' in html2:
            print("LOGIN SUCCESS")
        else:
            print("BAD LOGIN")

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
        #cmd_download(savedir=self.targetDir,skipextras=True,skipgames=False,skipids=False,dryrun=False,id=self.targetId,parent=self)
        pass
