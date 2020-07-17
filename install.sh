#!/bin/bash
apt-get install git -y
apt-get install python3-pil -y
apt-get install python-bs4 -y # or is it python3

git clone -C /home/pi/ https://github.com/hzeller/rpi-rgb-led-matrix.git
git clone -C /home/pi/ https://github.com/CodeSingh/rpi-led-scoreboard.git

cd /home/pi/rpi-rgb-led-matrix/bindings/python/
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

cd /home/pi/rpi-led-scoreboard/
sudo crontab cronjobs.txt







