#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import json
import os.path
import constants as c 

from datetime import datetime
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
import logging
from logging import handlers

DEFAULT_CLUB_CREST = '/home/pi/rpi-led-scoreboard/img/teams/default.png'  
WEATHER_JSON = '/home/pi/rpi-led-scoreboard/weather.json' 
ALL_TEAMS = "all"

class RunScoreboard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunScoreboard, self).__init__(*args, **kwargs)

    def run(self):
        score_team_home = ''
        score_team_away = ''
        image_home = None
        image_away = None
        match_status = ''
        match_start_time = ''

        while True:

            matrix = self.matrix
            matrix.Clear()

            valid_matches = False

            with open('/home/pi/rpi-led-scoreboard/config.json') as config_file:
                try:
                    config = json.load(config_file)
                    if config['state'] == "0":
                        time.sleep(60)
                        continue
                except ValueError as e:
                    logging.error("Ln: 46 " + str(e))
                    time.sleep(60)
                    continue
 
            # Single custom match setup
            if config['state'] == "2":
                with open('/home/pi/rpi-led-scoreboard/custom_matches.json') as json_file_custom_matches:
                    try:
                        data = json.load(json_file_custom_matches)
                    except ValueError as e:
                        logging.error("Ln: 56 " + str(e))
                        time.sleep(60)
                        continue
                for fixture in data:
                    single_match_display(matrix, fixture)
                continue

            with open('/home/pi/rpi-led-scoreboard/matches.json') as json_file:
                try:
                    data = json.load(json_file)
                    if config['state'] == "0":
                        time.sleep(60)
                        continue
                except ValueError as e:
                    logging.error("Ln: 68 " + str(valid_matches) + " " + str(e))
                    time.sleep(60)
                    continue

            if(config["team"] != ALL_TEAMS ): # pick out team if specified
                data = [x for x in data if x["team-home"] == config['team'] or x["team-away"] == config['team']]

            if(len(data) == 0): # No matches today
                if( os.path.getsize(WEATHER_JSON) > 0):
                    try:
                        with open(WEATHER_JSON) as json_file:
                            weather = json.load(json_file)

                        if 'main' in weather:
                            # Icon
                            weather_icon = "/home/pi/rpi-led-scoreboard/img/weather/icons/" + weather['weather'][0]['icon'] + ".png"
                            if os.path.isfile(weather_icon):
                                try:
                                    image_weather_icon = Image.open(weather_icon)
                                    matrix.SetImage(image_weather_icon.convert('RGB'), 0, 8)
                                except OSError as e:
                                    logging.error("Ln: 85 " + str(e))
                                except Exception as e:
                                    logging.error("Ln: 87 " + str(e))
                                # Temp
                                fontTemp = graphics.Font()
                                fontTemp.LoadFont("/home/pi/rpi-led-scoreboard/fonts/5x7.bdf")
                                yellow = graphics.Color(255, 255, 0)
                                temp = str(int(weather['main']['temp'])) + c.DICT_TEMP_TYPES[config["weather_api_units"]] 
                                graphics.DrawText(matrix, fontTemp, 40, 14, yellow, temp)

                                # Conditions
                                fontConditions = graphics.Font()
                                fontConditions.LoadFont("/home/pi/rpi-led-scoreboard/fonts/6x13B.bdf")
                                yellow = graphics.Color(255, 255, 0)
                                weather_conditions = weather['weather'][0]['main']
                                graphics.DrawText(matrix, fontConditions, 0, 10, yellow, weather_conditions)
                    except Exception as e:
                        logging.error("Ln: 107 " + str(e))
                    

                # Time
                fontTime = graphics.Font()
                fontTime.LoadFont("/home/pi/rpi-led-scoreboard/fonts/5x7.bdf")
                yellow = graphics.Color(255, 255, 0)
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                graphics.DrawText(matrix, fontTime, 40, 7, yellow, current_time)
                time.sleep(60)

            else:
                for fixture in data:
                    single_match_display(matrix, fixture)

def json_validator(data):
    try:
        json.loads(data.read())
        return True
    except ValueError as error:
        print("invalid json: %s" % error)
        return False

def single_match_display(_matrix, _fixture):
    _matrix.Clear()
    text_team_home = _fixture['team-home']
    text_team_away = _fixture['team-away']
    score_team_home = _fixture['score-home']
    score_team_away = _fixture['score-away']

    file_image_home = '/home/pi/rpi-led-scoreboard/img/teams/' + text_team_home + '.png'
    if os.path.isfile(file_image_home):
        image_home = Image.open(file_image_home)
    else:
        image_home = Image.open(DEFAULT_CLUB_CREST)

    file_image_away = '/home/pi/rpi-led-scoreboard/img/teams/' + text_team_away + '.png'
    if os.path.isfile(file_image_away):
        image_away = Image.open(file_image_away)
    else:
        image_away = Image.open(DEFAULT_CLUB_CREST)

    match_status = _fixture['status']
    match_start_time = _fixture['start-time']                
        
    _matrix.SetImage(image_home.convert('RGB'), -16, 0)
    _matrix.SetImage(image_away.convert('RGB'), 48, 0)

    fontScore = graphics.Font()
    fontScore.LoadFont("/home/pi/rpi-led-scoreboard/fonts/6x13B.bdf")
    yellow = graphics.Color(255, 255, 0)
    graphics.DrawText(_matrix, fontScore, 17, 10, yellow, "{0} - {1}".format(str(score_team_home), str(score_team_away) ) )

    green = graphics.Color(0, 255, 0)
    fontStatus = graphics.Font()
    fontStatus.LoadFont("/home/pi/rpi-led-scoreboard/fonts/6x13B.bdf")
    if match_status == "" :
        text_len = len(match_start_time)
        graphics.DrawText(_matrix, fontStatus, 32-(6* (text_len / 2)), 20, green, "{0}".format(match_start_time) )
    else:
        text_len = len(match_status)
        graphics.DrawText(_matrix, fontStatus, 32-(6* (text_len / 2)), 20, green, "{0}".format(match_status) )
    time.sleep(30)

# Main function
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', 
                        level=logging.INFO,
                        handlers=[
                            handlers.RotatingFileHandler(
                                    '/home/pi/rpi-led-scoreboard/scoreboard.log',
                                    maxBytes=10240, backupCount=3)
                        ]
                        )
    logging.info('Started')
    try:
        run_scoreboard = RunScoreboard()
        if (not run_scoreboard.process()):
            run_scoreboard.print_help()
    except Exception as e:
        logging.error("Ln: 180 " + str(e))
    logging.info('Finished')