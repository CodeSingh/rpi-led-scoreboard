#!/bin/bash
/usr/bin/timeout 60 /usr/bin/python3 /home/pi/rpi-led-scoreboard/score_update.py
/usr/bin/timeout 60 /usr/bin/python3 /home/pi/rpi-led-scoreboard/weather_update.py