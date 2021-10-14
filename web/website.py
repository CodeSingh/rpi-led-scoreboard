'''
Code based on work by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/
'''
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import datetime
import json
import os
import time
import pytz
import sys
sys.path.append('/home/pi/rpi-led-scoreboard/')
from config_update import get_config, set_config, get_custom_config, set_custom_config
import constants as c
from livescore_manager import LivescoreManager

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = '/home/pi/rpi-led-scoreboard/img/teams'
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG']
app.config['ALL_TIMEZONES'] = pytz.common_timezones

@app.route("/")
def index():
   livescore = LivescoreManager()
   competitions = livescore.get_competitions()
   model_index = { "teams" : c.DICT_TEAMS, "competitions": competitions, "data" : get_config(), "temp_types": c.DICT_TEMP_TYPES, "custom_matches": get_custom_config(), "timezones": app.config['ALL_TIMEZONES'] }

   print(model_index)
   return render_template('index.html', **model_index)

@app.route('/reboot',methods = ['POST'])
def reboot():
   if request.method == 'POST':
      os.system('sudo reboot')

      return redirect(url_for('index'))

@app.route('/shutdown',methods = ['POST'])
def shutdown():
   if request.method == 'POST':
      os.system('sudo shutdown -h now')

      return redirect(url_for('index'))

@app.route('/update',methods = ['POST'])
def update():
   if request.method == 'POST':
      os.system('sudo chown pi:pi ' + c.BASE_PATH_SCOREBOARD + '*')
      os.chdir(c.BASE_PATH_SCOREBOARD)
      os.system('sudo -u pi git fetch origin master')
      os.system('sudo -u pi git reset --hard FETCH_HEAD')
      os.system('sudo -u pi git clean -df')
      os.system('sudo apt-get install python3-tz -y')
      os.system('sudo -u pi cp /home/pi/rpi-led-scoreboard/config.json.example /home/pi/rpi-led-scoreboard/config.json')
      os.system('sudo reboot')

      return redirect(url_for('index'))

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
      config['timezone'] = request.form['timezone']

      create_config_files(config['state'])

      set_config(config)

   return redirect(url_for('index'))
   #else:
   #   user = request.args.get('nm')
   #   return redirect(url_for('success',name = user))

def create_config_files(state):
   if state == c.STATE_CUSTOM_MATCHES:
      if not os.path.isfile('/home/pi/rpi-led-scoreboard/custom_matches.json'):
         os.system('cp -a /home/pi/rpi-led-scoreboard/custom_matches.json.example /home/pi/rpi-led-scoreboard/custom_matches.json')

@app.route('/update_custom_matches',methods = ['POST'])
def update_custom_matches():
   print(request)
   if request.method == 'POST':
      headers = ('team-home', 'team-away', 'status', 'start-time', 'start-date', 'location', 'score-home', 'score-away')
      values = (
        request.form.getlist('team-home[]'),
        request.form.getlist('team-away[]'),
        request.form.getlist('status[]'),         
        request.form.getlist('start-time[]'),         
        request.form.getlist('start-date[]'),         
        request.form.getlist('location[]'), 
        request.form.getlist('score-home[]'), 
        request.form.getlist('score-away[]')             
      )
      
      items = [{} for i in range(len(values[0]))]
      for x,i in enumerate(values):
         for _x,_i in enumerate(i):
            items[_x][headers[x]] = _i
      config = items
      set_custom_config(config)
   return redirect(url_for('index'))

@app.route("/upload-image", methods=["POST"])
def upload_image():

   if request.method == "POST":

      if request.files:

         image = request.files["image"]

         if image.filename == "":
            print("No filename")
            return redirect(url_for('index'))

         if allowed_image(image.filename):
            filename = image.filename

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            os.chown(os.path.join(app.config["IMAGE_UPLOADS"], filename), 1000, 1000)

            print("Image saved")

            return redirect(url_for('index'))

         else:
            print("That file extension is not allowed")
            return redirect(url_for('index'))

@app.route('/team-uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['IMAGE_UPLOADS'],
                               filename, as_attachment=True)

def allowed_image(filename):

   # We only want files with a . in the filename
   if not "." in filename:
      return False

   # Split the extension from the filename
   ext = filename.rsplit(".", 1)[1]

   # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
   if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
      return True
   else:
      return False


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)