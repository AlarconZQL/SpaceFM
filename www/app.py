# Imports
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import datetime
import os

from flask import  flash, redirect, url_for
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'songs/'
ALLOWED_EXTENSIONS = set(['mp3','mp4','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

from models import Music
from database import Database


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = Database()
music = Music()


# Define the route to enter in the browser
@app.route('/')
def index():
    canciones = music.get_names_songs()
    return render_template('index2.html',canciones=canciones)

@app.route("/info")
def info():
    info = {
       "dato" : "aaaa"
    }
    return jsonify(info)

@app.route("/actualizar")
def actualizar():
    estados = {
       "song" : "Canción para Naufragios",
       "frecuency" : 95.3,
       "status" : "emiting"
    }
    return jsonify(estados)

@app.route("/borrar", methods = ["POST"])
def borrar():
    print("Borrando...")
    songsToDelete = request.get_json()
    app.logger.info(songsToDelete)
    for id in songsToDelete:
        music.delete_song(id)

    return jsonify(music.get_names_songs_json())




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if request.files == None:
        return "error 0"
    try:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error 1"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "error 2"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "uooo"
        else:
            return "NOOOOO"

    except Exception as e:
        return "Algo paso y dio Error"

"""

@app.route('/match', methods = ["POST"])
def start_match():

    # If there is a process running, return to index()
    if pro.is_running():
        return index()
    data = request.form
    d_m = {}
    d_m["team1"] = data["eastern"]
    d_m["team2"] = data["western"]
    d_m["place"] = data["place"]
    if (data["place"] == ""):
        d_m["place"] = "NEUTRAL"
    id_match = db.init_match(d_m)
    pro.start_process(d_m,id_match)
    return render_template('match.html',
                           id_team_east=d_m["team1"], id_team_west=d_m["team2"], id_match=id_match)

@app.route('/match/stop/<id_match>', methods = ["GET"])
def stop_match(id_match):
    data = pro.stop_process()
    return jsonify({"status": data})

@app.route('/result/match/<id_match>', methods = ["GET"])
def get_result_match(id_match):
    result_match = db.get_result_match(id_match)
    return jsonify(result_match)

@app.route('/match/<id_match>', methods = ["GET"])
def get_match(id_match):
    match = db.get_match(id_match)
    return jsonify(match)

@app.route('/team/<id_team>', methods = ["GET"])
def get_team(id_team):
    team = db.get_team(id_team)
    return jsonify(team)
"""


if __name__ == "__main__":
    # Define HOST and port
    app.run(host='0.0.0.0', port=8888)
