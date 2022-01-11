#!/usr/bin/env python3
import sys
import json
from datetime import datetime, timezone
import pytz
import constants as c
from livescore_manager import LivescoreManager
import logging
from logging import handlers

logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', level=logging.INFO,
                    handlers=[
                        handlers.RotatingFileHandler(
                                '/home/pi/rpi-led-scoreboard/score.log',
                                maxBytes=10240, backupCount=3)
                    ]
                    )


def get_config():
    PATH_TO_CONFIG_JSON = '/home/pi/rpi-led-scoreboard/config.json'
    with open(PATH_TO_CONFIG_JSON, 'r') as jsonfile:
        json_content = json.load(jsonfile)
        return json_content


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.tzname).astimezone(tz=None)


def main():
    # read existing json to memory. you do this to preserve whatever existing data. 
    config = get_config()
    all_matches(config["live_score_type"])


def all_matches(live_score_type):
    ALL_TEAMS = "all"
    PATH_TO_ALL_MATCHES_JSON = '/home/pi/rpi-led-scoreboard/matches.json'

    livescore = LivescoreManager()
    livescore_class = livescore.get_live_score_class(live_score_type, ALL_TEAMS)
    logging.info("All Matches")
    api_fixture = livescore_class.get_all_fixtures()
    logging.info("After all fixtures")
    gmt = pytz.timezone('GMT')
    user_tz = get_user_tz()

    for fixture in api_fixture:
        logging.info(fixture["start-time"])
        if fixture["start-time"] != "":
            logging.info(fixture["start-time"])

            start_time = datetime.strptime(fixture["start-time"] + " 1980", '%H:%M %Y')
            gmt_start_time = gmt.localize(start_time)

            user_start_time = gmt_start_time.astimezone(user_tz)
            fixture["start-time"] = user_start_time.strftime("%H:%M")

    with open(PATH_TO_ALL_MATCHES_JSON,'w') as jsonfile:
        json.dump(api_fixture, jsonfile, indent=4)  # you decide the indentation level


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

    if api_fixture["start-time"] != "":
        gmt = pytz.timezone('GMT')
        start_time = datetime.strptime(api_fixture["start-time"], '%H:%M')
        gmt_start_time = gmt.localize(start_time)
        user_tz = get_user_tz()

        user_start_time = gmt_start_time.astimezone(user_tz)

        json_content["start-time"] = user_start_time

    with open(PATH_TO_MATCH_JSON, 'w') as jsonfile:
        json.dump(json_content, jsonfile, indent=4)  # you decide the indentation level


def get_user_tz():
    config = get_config()
    return pytz.timezone(config['timezone'])

if __name__ == "__main__":
    logging.info('Started')
    try:
        main()
    except Exception as e:
        logging.error(str(e))
    logging.info('Finished')
