# Imports
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from utils import RadioManager
from exceptions import FileFormatNotAllowedError

app = Flask(__name__)
radio_manager = RadioManager()

# Ruta raiz que carga el contenido principal de la pagina
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para consultar el estado de la emisora
@app.route("/actualizar")
def actualizar():
    estados = {
       "song" : "Canción para Naufragios",
       "frecuency" : 95.3,
       "status" : "emiting"
    }
    return jsonify(estados)

# Ruta para eliminar un conjunto de archivos de audio
@app.route("/borrar", methods = ["POST"])
def borrar():
    songsToDelete = request.get_json()    
    for id in songsToDelete:
        app.logger.info("Borrando archivo: " + id)
        if radio_manager.delete_song(id):
            app.logger.info("Exito al borrar")
        else:
            app.logger.info("No existe el archivo")
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
        if radio_manager.save_song(file):
            app.logger.info('Archivo guardado con exito')                
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
