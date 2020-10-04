#!/usr/bin/env python
import json
import requests
import sys
import os.path
from PIL import Image
import logging
from logging import handlers
     
def get_config():
    PATH_TO_CONFIG_JSON = '/home/pi/rpi-led-scoreboard/config.json' 
    with open(PATH_TO_CONFIG_JSON,'r') as jsonfile:
        json_content = json.load(jsonfile)
        return json_content
     
def get_weather(url, api_key, location, units):
    url = url.format(location, api_key, units)
    r = requests.get(url)
    return r.json()

def get_icon(url, dest_file):

    with open(dest_file, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)

    image = Image.open(dest_file) 
    MAX_SIZE = (30, 30) 
    
    image.thumbnail(MAX_SIZE) 
        
    # creating thumbnail 
    image.save(dest_file) 


def main():

    PATH_TO_WEATHER_JSON = '/home/pi/rpi-led-scoreboard/weather.json'
    URL_ICON = "http://openweathermap.org/img/w/{0}.png"
    PATH_ICON = "/home/pi/rpi-led-scoreboard/img/weather/icons/{0}.png"
    INCORRECT_API_KEYS = ['', 'XXX']

    config = get_config()
    location = config['weather_location']
    units = config['weather_api_units']
    api_key = config['weather_api_key']
    url = config['weather_api_url']

    if api_key not in INCORRECT_API_KEYS:
        weather = get_weather(url, api_key, location, units)
        
        if 'weather' in weather:
            icon_url = URL_ICON.format(weather['weather'][0]['icon'])
            icon_path = PATH_ICON.format(weather['weather'][0]['icon'])
            get_icon(icon_url, icon_path)
            logging.info('Got weather')

        with open(PATH_TO_WEATHER_JSON,'w') as jsonfile:
            json.dump(weather , jsonfile, indent=4)
 
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', level=logging.INFO,
                        handlers=[
                            handlers.RotatingFileHandler(
                                    '/home/pi/rpi-led-scoreboard/weather.log',
                                    maxBytes=10240, backupCount=3)
                        ]
                        )
    logging.info('Started')
    try:
        main()
    except Exception as e:
        logging.error(str(e))
    logging.info('Finished')