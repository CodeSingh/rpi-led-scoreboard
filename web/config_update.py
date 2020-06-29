
from urllib.request import urlopen
import time
import sys
import json
from datetime import datetime
import os
import constants as c


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

