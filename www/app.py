# Imports
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from utils import RadioManager
from utils import RadioProcess

from exceptions import FileFormatNotAllowedError

app = Flask(__name__)
radio_manager = RadioManager()
radioProcess = RadioProcess()

# Ruta raiz que carga el contenido principal de la pagina
@app.route('/')
def index():
    return render_template('index.html')

import subprocess
import os


# Ruta para iniciar la emisora
@app.route("/start", methods = ["POST"])
def start():
    app.logger.info("Iniciando proceso...")
    #app.logger.info(pro.start_process())

    """
    cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/heroe.wav"
    pwd = "raspberry"
    #preexec_fn=os.setsid
    #fpid = os.fork()
    #fpid=0
    #command = './home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/heroe.wav'.split()
    #subprocess.Popen(command, shell=True)

    command = 'python3 anda.py'.split()
    subprocess.Popen(command)
        cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/heroe.wav"
        pwd = "raspberry"

        app.logger.info("A")
        p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)

    """
    """
    f = open("comunicar.txt", "w")
    f.write("Iniciar")
    f.close()
    """
    radioProcess.start()

    return "sarasa"

# Ruta para detener la emisora
@app.route("/stop", methods = ["POST"])
def stop():
    """
    f = open("comunicar.txt", "w")
    f.write("Detener")
    f.close()
    """
    radioProcess.stop()

    return "parado"

# Ruta para detener la emisora
@app.route("/next", methods = ["POST"])
def next():
    """
    f = open("comunicar.txt", "w")
    f.write("Siguiente")
    f.close()
    """
    radioProcess.next()

    return "parado"

# Ruta para consultar el estado de la emisora
@app.route("/actualizar")
def actualizar():
    return jsonify(radioProcess.getState())

# Ruta para eliminar un conjunto de archivos de audio
@app.route("/borrar", methods = ['DELETE'])
def borrar():
    songsToDelete = request.get_json()
    for id in songsToDelete:
        app.logger.info("Borrando archivo: " + id)
        if radio_manager.delete_song(id):
            app.logger.info("Exito al borrar")
        else:
            app.logger.info("No existe el archivo")
    radioProcess.update()
    return jsonify(songs_list = radio_manager.get_names_songs_json())

# Ruta para subir a la emisora un conjunto de archivos de audio
@app.route('/upload', methods=['POST'])
def upload():
    if request.files == None:
        return "No se adjunto ningun archivo"
    try:
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(error_msg = "No se encuentra el archivo en el requerimiento")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify(error_msg = "Nombre de archivo vacio")
        app.logger.info('Guardando archivo: ' + file.filename + '...')
        file.filename = file.filename.replace(' ','-')
        if radio_manager.save_song(file):
            nombre = file.filename
            nombre2 = nombre.replace('mp3','wav')
            cmd = 'sox songs/' + nombre + ' -r 22050 -c 1 -b 16 -t wav songs/' + nombre2
            print('Ejecutando: ' + cmd)
            pwd = 'raspberry'
            p = subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
            cmd = 'rm songs/' + nombre
            pwd = 'raspberry'
            p = subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
            app.logger.info('Archivo guardado con exito')
            radioProcess.update()
        return jsonify(songs_list = radio_manager.get_names_songs_json())
    except FileFormatNotAllowedError as e:
        app.logger.error('Formato de archivo no soportado')
        return jsonify(error_msg = str(e))
    except Exception as e:
        return jsonify(error_msg = str(e))

# Ruta para obtener todos los archivos de audio almacenadas en la emisora
@app.route('/listar', methods=['GET'])
def listar_canciones():
    app.logger.info('Listando canciones ...')
    return jsonify(songs_list = radio_manager.get_names_songs_json())

if __name__ == "__main__":
    # Define HOST and port
    app.run(host='0.0.0.0', port=8888)
