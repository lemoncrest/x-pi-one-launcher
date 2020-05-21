Needs if you don't want an error (raspbian)

libatlas-base-dev
libglib2.0-dev
python-dbus-dev

in python3 (python2 is deprecated)

pip install -r requirements

#music can be download with this command at the original page (free distribution):
curl https://patrickdearteaga.com/chiptune-8-bit-retro/ | grep -E "(https?:)?//[^/\s]+/\S+\.(ogg|mp3)\"" -o | sed "s/^(https?)?\/\//https\:\/\//g" -r | sed -r 's/[\"]+//g' > url.txt && wget -i url.txt -P assert/music/ && rm url.txt
curl https://patrickdearteaga.com/arcade-music/ | grep -E "(https?:)?//[^/\s]+/\S+\.(ogg|mp3)\"" -o | sed "s/^(https?)?\/\//https\:\/\//g" -r | sed -r 's/[\"]+//g' >url.txt && wget -i url.txt -P assert/music/ && rm url.txt
