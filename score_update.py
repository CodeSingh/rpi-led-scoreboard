#!/usr/bin/env python3
import sys
import json
import constants as c
from livescore_manager import LivescoreManager

def get_config():
    PATH_TO_CONFIG_JSON = '/home/pi/scoreboard/config.json' 
    with open(PATH_TO_CONFIG_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile)
        return json_content

def main():
    PATH_TO_MATCH_JSON = '/home/pi/scoreboard/match.json' 
    # read existing json to memory. you do this to preserve whatever existing data. 
    with open(PATH_TO_MATCH_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile) # this is now in memory! you can use it outside 'open'

    config = get_config()

    livescore = LivescoreManager()
    livescore_class = livescore.get_live_score_class(config["live_score_type"], config["team"])
    api_fixture = livescore_class.get_live_score()

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
    main()