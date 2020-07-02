#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import sys
import json
from datetime import datetime
import os
import constants as c
from livescore_manager import LivescoreManager
import score_update
import weather_update

PATH_TO_CONFIG_JSON = '/home/pi/rpi-led-scoreboard/config.json' 

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_config():
    with open(PATH_TO_CONFIG_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile)
        return json_content

def set_config(json_content):
    with open(PATH_TO_CONFIG_JSON,'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4) # you decide the indentation level    



if __name__ == "__main__":
    config = get_config()
    while True:
        clear_term()
        print("********** Config Updater **********\n")
        config["state"] = input("Turn ON/OFF [0 = OFF] and [1 = ON]\nCurrent:[" + config["state"] + "]:") or config["state"]

        current_team_no = 0
        for key, value in c.DICT_TEAMS.items():
            print(key, '->', value)
            if(value == config["team"]):
                current_team_no = key

        team_no = int(input("Choose Team name number\nCurrent:[" + config["team"] + "]:") or current_team_no)

        print(c.DICT_TEAMS[team_no])

        config["team"] =  c.DICT_TEAMS[team_no]

        current_competition = 0
        livescore = LivescoreManager()
        competitions = livescore.get_competitions()
        
        inc = 0
        for competition in competitions:
            print(str(inc) + " -> " + competition.Name)
            if(value == config["live_score_type"]):
                current_competition = inc
            inc = inc + 1

        competition_no = int(input("Choose competition\nCurrent:[" + config["live_score_type"] + "]:") or current_competition)
        print(competitions[competition_no])
        config["live_score_type"] = competitions[competition_no].ID

        config["weather_location"] = input("Enter your location (for weather display)\nCurrent:[" + config["weather_location"] + "]:") or config["weather_location"]
        
        break

    set_config(config)
    print("********** Updating score and weather settings **********\n")
    score_update.main()
    weather_update.main()
    print("********** It can take up to a minute to refresh the scoreboard  **********\n")