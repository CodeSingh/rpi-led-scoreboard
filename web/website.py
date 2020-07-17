'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
from flask import Flask, render_template, request, redirect, url_for
import datetime
import json
import os
import time
import sys
sys.path.append('/home/pi/rpi-led-scoreboard/')
from config_update import get_config, set_config
import constants as c
from livescore_manager import LivescoreManager


app = Flask(__name__)
@app.route("/")
def index():
   livescore = LivescoreManager()
   competitions = livescore.get_competitions()
   model_index = { "teams" : c.DICT_TEAMS, "competitions": competitions, "data" : get_config(), "temp_types": c.DICT_TEMP_TYPES}

   print(model_index)
   return render_template('index.html', **model_index)

@app.route('/reboot',methods = ['POST'])
def reboot():
   if request.method == 'POST':
      os.system('sudo reboot')
      time.sleep(5)
      return redirect(url_for('index'))
   #else:
   #   user = request.args.get('nm')
   #   return redirect(url_for('success',name = user))

@app.route('/save',methods = ['POST'])
def save():
   if request.method == 'POST':
      config = get_config()
      config['state'] = request.form['state']
      config['team'] = request.form['team']
      config['weather_location'] = request.form['weather_location']
      config['live_score_type'] = request.form['live_score_type']
      config['weather_api_key'] = request.form['weather_api_key']
      config['weather_api_units'] = request.form['weather_api_units']

      
      set_config(config)

   return redirect(url_for('index'))
   #else:
   #   user = request.args.get('nm')
   #   return redirect(url_for('success',name = user))

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)