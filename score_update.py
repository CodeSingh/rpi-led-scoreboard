#!/usr/bin/env python3
import sys
import json
import constants as c
from livescore_manager import LivescoreManager
import logging
from logging import handlers

def get_config():
    PATH_TO_CONFIG_JSON = '/home/pi/rpi-led-scoreboard/config.json' 
    with open(PATH_TO_CONFIG_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile)
        return json_content

def main():
    # read existing json to memory. you do this to preserve whatever existing data. 
    config = get_config()
    all_matches(config["live_score_type"])


    
def all_matches(live_score_type):
    ALL_TEAMS = "all"
    PATH_TO_ALL_MATCHES_JSON = '/home/pi/rpi-led-scoreboard/matches.json'

    livescore = LivescoreManager()
    livescore_class = livescore.get_live_score_class(live_score_type, ALL_TEAMS)
    api_fixture = livescore_class.get_all_fixtures()

    with open(PATH_TO_ALL_MATCHES_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile) # this is now in memory! you can use it outside 'open'

    # add the id key-value pair (rmbr that it already has the "name" key value)
    json_content = api_fixture

    with open(PATH_TO_ALL_MATCHES_JSON,'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4) # you decide the indentation level

def single_match(live_score_type, team):
    PATH_TO_MATCH_JSON = '/home/pi/rpi-led-scoreboard/match.json' 
    
    livescore = LivescoreManager()
    livescore_class = livescore.get_live_score_class(live_score_type, team)
    api_fixture = livescore_class.get_live_score()

    with open(PATH_TO_MATCH_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile) # this is now in memory! you can use it outside 'open'

    # add the id key-value pair (rmbr that it already has the "name" key value)
    json_content["team-home"] = api_fixture["team-home"]            
    json_content["team-away"] = api_fixture["team-away"]
    json_content["score-home"] = api_fixture["score-home"]
    json_content["score-away"] = api_fixture["score-away"]
    json_content["status"] = api_fixture["status"]
    json_content["start-time"] = api_fixture["start-time"]

    with open(PATH_TO_MATCH_JSON,'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4) # you decide the indentation level

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', level=logging.INFO,
                        handlers=[
                            handlers.RotatingFileHandler(
                                    '/home/pi/rpi-led-scoreboard/score.log',
                                    maxBytes=10240, backupCount=3)
                        ]
                        )
    logging.info('Started')
    try:
        main()
    except Exception as e:
        logging.error(str(e))
    logging.info('Finished')