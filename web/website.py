'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
from flask import Flask, render_template, request, redirect, url_for
import datetime
import json
import os
from config_update import get_config, set_config
import constants as c
import time

app = Flask(__name__)
@app.route("/")
def index():
   model_index = { "teams" : c.DICT_TEAMS, "data" : get_config() }

   print(model_index)
   return render_template('index.html', **model_index)

@app.route('/reboot',methods = ['POST'])
def reboot():
   if request.method == 'POST':
      os.system('sudo reboot')
      time.sleep(10)
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
      set_config(config)

   return redirect(url_for('index'))
   #else:
   #   user = request.args.get('nm')
   #   return redirect(url_for('success',name = user))

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)