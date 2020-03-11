#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import json
import os.path

from datetime import datetime
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
#4x6.bdf
class RunScoreboard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunScoreboard, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        DEFAULT_CLUB_CREST = '/home/pi/scoreboard/img/teams/default.png'  
        WEATHER_JSON = '/home/pi/scoreboard/weather.json'
        DEFAULT_STATUS = 'No Game'    

        text_team_home = ''
        text_team_away = ''
        score_team_home = ''
        score_team_away = ''
        image_home = None
        image_away = None
        match_status = ''
        match_start_time = ''

        while True:

            matrix = self.matrix
            matrix.Clear()

            with open('/home/pi/scoreboard/config.json') as json_file:
                data = json.load(json_file)
                if data['state'] == "0":
                    time.sleep(60)
                    continue

            with open('/home/pi/scoreboard/match.json') as json_file:
                data = json.load(json_file)

                text_team_home = data['team-home']
                text_team_away = data['team-away']
                score_team_home = data['score-home']
                score_team_away = data['score-away']

                file_image_home = '/home/pi/scoreboard/img/teams/' + data['team-home'] + '.png'
                if os.path.isfile(file_image_home):
                    image_home = Image.open(file_image_home)
                else:
                    image_home = Image.open(DEFAULT_CLUB_CREST)

                file_image_away = '/home/pi/scoreboard/img/teams/' + data['team-away'] + '.png'
                if os.path.isfile(file_image_away):
                    image_away = Image.open(file_image_away)
                else:
                    image_away = Image.open(DEFAULT_CLUB_CREST)

                match_status = data['status']
                match_start_time = data['start-time']
            # Weather
            if match_status == DEFAULT_STATUS:                
                with open(WEATHER_JSON) as json_file:
                    weather = json.load(json_file)

                    if 'main' in weather:
                        # Icon
                        weather_icon = "/home/pi/scoreboard/img/weather/icons/" + weather['weather'][0]['icon'] + ".png"
                        if os.path.isfile(weather_icon):
                            image_weather_icon = Image.open(weather_icon)
                            matrix.SetImage(image_weather_icon.convert('RGB'), 0, 8)

                        # Temp
                        fontTemp = graphics.Font()
                        fontTemp.LoadFont("/home/pi/scoreboard/fonts/5x7.bdf")
                        yellow = graphics.Color(255, 255, 0)
                        temp = str(int(weather['main']['temp'])) + '\'C' 
                        graphics.DrawText(matrix, fontTemp, 50, 14, yellow, temp)

                        # Conditions
                        fontConditions = graphics.Font()
                        fontConditions.LoadFont("/home/pi/scoreboard/fonts/6x13B.bdf")
                        yellow = graphics.Color(255, 255, 0)
                        weather_conditions = weather['weather'][0]['main']
                        graphics.DrawText(matrix, fontConditions, 0, 10, yellow, weather_conditions)

                    # Time
                    fontTime = graphics.Font()
                    fontTime.LoadFont("/home/pi/scoreboard/fonts/5x7.bdf")
                    yellow = graphics.Color(255, 255, 0)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    graphics.DrawText(matrix, fontTime, 40, 7, yellow, current_time)
                    
            else:
                matrix.SetImage(image_home.convert('RGB'), -16, 0)
                matrix.SetImage(image_away.convert('RGB'), 48, 0)

                fontScore = graphics.Font()
                fontScore.LoadFont("/home/pi/scoreboard/fonts/6x13B.bdf")
                yellow = graphics.Color(255, 255, 0)
                graphics.DrawText(matrix, fontScore, 17, 10, yellow, "{0} - {1}".format(str(score_team_home), str(score_team_away) ) )

                green = graphics.Color(0, 255, 0)
                fontStatus = graphics.Font()
                fontStatus.LoadFont("/home/pi/scoreboard/fonts/6x13B.bdf")
                if match_status == "" :
                    graphics.DrawText(matrix, fontStatus, 17, 22, green, "{0}".format(match_start_time) )
                else:
                    graphics.DrawText(matrix, fontStatus, 26, 22, green, "{0}".format(match_status) )
        
            time.sleep(60)

# Main function
if __name__ == "__main__":
    run_scoreboard = RunScoreboard()
    if (not run_scoreboard.process()):
        run_scoreboard.print_help()

