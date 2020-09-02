This repository is not finished launcher for LemonPi project. 

If you want to know more about LemonPi project please go to the https://lemoncrest.com/products section and suscribe for news

This launcher is coded un python and will show you more options when it's finished. Feel free to open issues and test.

Needs if you don't want an error (raspbian)

libatlas-base-dev
libglib2.0-dev
python-dbus-dev

in python3 (python2 is deprecated)

pip install -r requirements

#music can be download with this command at the original page (free distribution):

curl https://patrickdearteaga.com/chiptune-8-bit-retro/ | grep -E "(https?:)?//[^/\s]+/\S+\.(ogg|mp3)\"" -o | sed "s/^(https?)?\/\//https\:\/\//g" -r | sed -r 's/[\"]+//g' > url.txt && wget -i url.txt -P assert/music/ && rm url.txt

curl https://patrickdearteaga.com/arcade-music/ | grep -E "(https?:)?//[^/\s]+/\S+\.(ogg|mp3)\"" -o | sed "s/^(https?)?\/\//https\:\/\//g" -r | sed -r 's/[\"]+//g' >url.txt && wget -i url.txt -P assert/music/ && rm url.txt
