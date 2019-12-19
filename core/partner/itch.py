import http.cookiejar
import urllib
import logging
import os
#logging.basicConfig(filename=os.path.join(os.getcwd(), "log.txt"), level=logging.DEBUG)
logger = logging.getLogger(__name__)
import requests
import json

class Itch():

    LOGIN_URL = 'https://itch.io/login'
    PURCHASES = 'https://itch.io/my-purchases'

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def login2(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://itch.io',
            'Referer': Itch.LOGIN_URL
        }

        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        urllib.request.install_opener(opener)

        response = urllib.request.urlopen(url=Itch.LOGIN_URL)

        html = response.read().decode('utf-8')

        #seek for csrf
        csrf = html[:html.find('" name="csrf_token" type="hidden"/>')]
        csrf = csrf[csrf.rfind('<input value="')+len('<input value="'):]

        form = {
            "csrf_token" : urllib.parse.quote_plus(csrf),
            "username" : self.username,
            "password" : self.password
        }

        cookies = ""

        for key,value in response.info().items():
            if key.lower() == 'set-cookie':
                #cookie = value
                cookie = (value[0:value.find(" Path=/;")]+" ")
                if 'Expires=' in cookie:
                    cookie = cookie[0:cookie.find('Expires=')]
                cookies+= cookie


        headers = {}
        headers["Cookie"] = cookies #urllib.parse.unquote(cookies).replace("\n","")
        print(".."+headers["Cookie"]+"..")

        data = urllib.parse.urlencode(form).encode('utf-8')
        print(data)
        #request = urllib.request.Request(url=Itch.LOGIN_URL, data=data)
        #request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        #response = urllib.request.urlopen(request)
        response = urllib.request.urlopen(url=Itch.LOGIN_URL,data=data)

        html2 = response.read().decode('utf-8')
        print(html2)


    def login(self):
        self.session = requests.Session()
        response = self.session.get(Itch.LOGIN_URL)
        html = response.text
        # seek for csrf
        csrf = html[:html.find('" name="csrf_token" type="hidden"/>')]
        csrf = csrf[csrf.rfind('<input value="') + len('<input value="'):]

        form = {
            "csrf_token": csrf,
            "username": self.username,
            "password": self.password
        }

        self.session.post(url=Itch.LOGIN_URL,data=form)

    def getGames(self):
        if self.session is None:
            self.login()
        response = self.session.get(Itch.PURCHASES)
        html = response.text
        table = html[html.find('<div class="purchase_game_grid_widget game_grid_widget">')+len('<div class="purchase_game_grid_widget game_grid_widget">'):]
        table = table[:table.find('</div><div class="border_mask">')]
        i=0
        games = []
        for field in table.split('<div data-game_id="'):
            if i>0:
                game = {}
                title = field[field.find('class="title game_link">')+len('class="title game_link">'):]
                title = title[:title.find('<')]
                link = field[field.find(' href="') + len(' href="'):]
                link = link[:link.find('"')]
                image = field[field.find('background-image: url(&#039;') + len('background-image: url(&#039;'):]
                image = image[:image.find('&#039;)"')]
                if '<div class="game_platform">' in field:
                    platforms = []
                    j = 0
                    for field2 in field.split('<span title="Download for '):
                        if j>0:
                            platform = field2[:field2.find('"')].lower()
                            platforms.append(platform)
                            print(platform)
                        j+=1
                    game["platforms"] = platforms

                game["title"] = title
                game["link"] = link
                game["image"] = image
                games.append(game)
            i+=1

        return games


    def downloadGame(self,link,platform='linux'):
        if self.session is None:
            self.login()
        response = self.session.get(url=link)
        html = response.text
        i=0
        #id
        id = ""
        for field in html.split('<div class="upload">'):
            if i>0:
                if platform.lower() in field.lower():
                    id = field[field.find(' data-upload_id="')+len(' data-upload_id="'):]
                    id = id[:id.find('"')]
            i+=1
        print(id)
        #key
        key = html.split('{"key":"')[1]
        key=key[:key.find('"')]
        print(key)
        slug = html.split('"slug":"')[1]
        slug=slug[:slug.find('"')]
        print(slug)
        #now build url
        link2 = link[:link.find('download/')]
        link2+="file/"+id+"?key="+key
        print(link2)

        response2 = self.session.post(url=link2)
        html2 = response2.text
        print(html2)
        jsonloaded = json.loads(html2)
        print(jsonloaded["url"])
        return jsonloaded["url"]


