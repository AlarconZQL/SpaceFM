from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from radio import GestorArchivos
from radio import ReproductorRadio

from exceptions import FileFormatNotAllowedError

app = Flask(__name__)
gestor_archivos = GestorArchivos()
reproductor_radio = ReproductorRadio()

# Ruta raiz que carga el contenido principal de la pagina
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para reproducir una cancion
@app.route("/play", methods = ["GET"])
def play():
    reproductor_radio.reproducir_cancion()
    return "200"

# Ruta para detener la cancion actual
@app.route("/stop", methods = ["GET"])
def stop():
    reproductor_radio.detener_cancion()
    return "200"

# Ruta para pasar al siguiente tema en la emisora
@app.route("/next", methods = ["GET"])
def next():
    reproductor_radio.siguiente_cancion()
    return "200"

# Ruta para pasar al anterior tema en la emisora
@app.route("/prev", methods = ["GET"])
def prev():
    reproductor_radio.anterior_cancion()
    return "200"

# Ruta para consultar el estado de la emisora
@app.route("/update", methods=['GET'])
def update():
    return jsonify(reproductor_radio.estado_emisora())

# Ruta para eliminar un conjunto de archivos de audio
@app.route("/delete", methods = ['DELETE'])
def delete():
    songs_to_delete = request.get_json()
    for id in songs_to_delete:
        print("Borrando archivo con id: " + id)
        if gestor_archivos.borrar_cancion(id):
            print("Exito al borrar")
        else:
            print("No existe el archivo")
    reproductor_radio.actualizar_canciones()
    return jsonify(songs_list = gestor_archivos.listar_canciones_json())

# Ruta para subir a la emisora un conjunto de archivos de audio
@app.route('/upload', methods=['POST'])
def upload():
    if request.files == None:
        return "No se adjunto ningun archivo"
    msj_error = ""
    for requerimiento in request.files:
        try:
            archivo = request.files[requerimiento]
            # chequeamos si se encuentra este archivo dentro del requerimiento
            if requerimiento not in request.files:
                msj_error = msj_error + "No se encuentra el archivo " + requerimiento + " en el requerimiento\n"
            # chequeamos si el nombre del archivo esta vacio
            if archivo.filename == '':
                msj_error = msj_error + "Nombre de archivo vacio" + archivo.filename + "\n"
            gestor_archivos.guardar_cancion(archivo)
        except FileFormatNotAllowedError as e:
            msj_error = msj_error + 'Formato de archivo ' + archivo.filename +' no soportado\n'
        except Exception as e:
            msj_error = msj_error + 'Archivo ' + requerimiento + ' no pudo ser guardado \n'
    reproductor_radio.actualizar_canciones()
    if msj_error != "":
        print(msj_error)
    return jsonify(songs_list = gestor_archivos.listar_canciones_json())

# Ruta para obtener todos los archivos de audio almacenadas en la emisora
@app.route('/songs', methods=['GET'])
def get_songs():
    return jsonify(songs_list = gestor_archivos.listar_canciones_json())

if __name__ == "__main__":
    # Define HOST and port
    app.run(host='0.0.0.0', port=8888)
