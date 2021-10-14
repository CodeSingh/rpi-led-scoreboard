#!/bin/bash
sudo apt-get install python3-pil -y
sudo apt-get install python3-bs4 -y
sudo apt-get install python3-flask -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-tz -y

cd /home/pi/
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git # Not sudo so that changes can be made easily after install

cd /home/pi/rpi-rgb-led-matrix/
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
sudo make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)

cd /home/pi/rpi-led-scoreboard/
cp config.json.example config.json
sudo chmod 666 config.json
sudo crontab cronjobs.txt

cd /etc/modprobe.d/
sudo touch raspi-blacklist.conf
sudo sh -c " echo 'blacklist snd_bcm2835' >> raspi-blacklist.conf"