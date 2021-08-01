This repository is not finished launcher for old LemonPi project, but will be used to develop an interface for ArchLinuxARM running on X-PI.ONE portable device.

Note that LemonPi project was cancelled in 2020 and this repository has been forked to continue the current work for the new X-PI.ONE and get a launcher to configure somethings.

If you want a terminated launcher to learn howto do all components and things, use the Kelboy 2.x official launcher for Kelboy 2.x kits at https://github.com/lemoncrest/kelboy-launcher

Developers doesn't support anything with this repository, so feel free to read, develop, fork and make pull requests as you want, but no support could be received.

If you want to know more about X-PI.ONE project please go to the https://x-pi.one section and suscribe for news.

This launcher is coded under Python3 and pygame 2.0.1 (SDL 2.0.14, Python 3.9.6) framework and will show you more options when it's finished.

Needs if you don't want an error (raspbian and similars distros based on Computer Module 4 platforms)

libatlas-base-dev
libglib2.0-dev
python-dbus-dev

Use python3 with pip:

pip install -r requirements.txt

We recommend ArchLinuxArm like a beautiful, powerfull and strong platform to run this software, if you want to know more please use this https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-4 wiki page.

#core.partner path are reserved for external scripts providers, this scripts depends of externals platforms so feel free to enjoy with the code ;)

#wallpapers are copyleft pixelart png/jpg

#resources like music are copyleft, if you want them you can download all with this command at the original page (free distribution):

curl https://patrickdearteaga.com/chiptune-8-bit-retro/ | grep -E "(https?:)?//[^/\s]+/\S+\.(ogg|mp3)\"" -o | sed "s/^(https?)?\/\//https\:\/\//g" -r | sed -r 's/[\"]+//g' > url.txt && wget -i url.txt -P assert/music/ && rm url.txt

curl https://patrickdearteaga.com/arcade-music/ | grep -E "(https?:)?//[^/\s]+/\S+\.(ogg|mp3)\"" -o | sed "s/^(https?)?\/\//https\:\/\//g" -r | sed -r 's/[\"]+//g' >url.txt && wget -i url.txt -P assert/music/ && rm url.txt
