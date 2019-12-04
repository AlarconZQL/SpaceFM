import os
import signal
import subprocess
import threading
import sys
import re
import time

from werkzeug.utils import secure_filename
from exceptions import FileFormatNotAllowedError
from models import Song
from utils import SongEncoder

class GestorArchivos():

    DIRECTORIO_ARCHIVOS = 'musica/'
    EXTENSIONES_SOPORTADAS = set(['mp3','wav'])

    def __init__(self):
        pass    

    def listar_canciones_json(self):
        file_list = []
        k = 1
        for root, folders, files in os.walk(GestorArchivos.DIRECTORIO_ARCHIVOS):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(wav)$", filename) != None:
                    file_list.append(SongEncoder().encode(Song(k,filename)))
                    k = k + 1
        return file_list

    def borrar_cancion(self,name):
        if os.path.exists(GestorArchivos.DIRECTORIO_ARCHIVOS+name):
          os.remove(GestorArchivos.DIRECTORIO_ARCHIVOS+name)
          return True
        else:
          return False    

    def guardar_cancion(self,file):
        file.filename = file.filename.replace(' ','-')
        if file and self.__archivo_soportado(file.filename):
            filename = secure_filename(file.filename)
            print('Guardando archivo ' + filename)
            file.save(os.path.join(GestorArchivos.DIRECTORIO_ARCHIVOS, filename))
            if filename.rsplit('.', 1)[1].lower() != 'wav':
                self.__convertir_a_wav(filename)
            return True
        else:
            raise FileFormatNotAllowedError("Formato de archivo no soportado")
    
    def __archivo_soportado(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.EXTENSIONES_SOPORTADAS

    def __convertir_a_wav(self,filename):
        print('Convirtiendo ' + filename + ' a wav...')
        nombre_wav = filename.replace('mp3','wav')
        cmd = 'sox ' + GestorArchivos.DIRECTORIO_ARCHIVOS + filename + ' -r 22050 -c 1 -b 16 -t wav ' + GestorArchivos.DIRECTORIO_ARCHIVOS + nombre_wav
        pwd = 'raspberry'
        # Crear un nuevo archivo .wav
        p = subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
        cmd = 'rm ' + GestorArchivos.DIRECTORIO_ARCHIVOS + filename
        # Borrar el archivo original
        p = subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
        print('Archivo  ' + nombre_wav + ' guardado con exito!')

class ReproductorRadio(object):    

    def __init__(self):
        self.songs = None
        self.indice = None
        self.currentSong = None
        self.actualizar_canciones()
        self.frequency = 87.5
        self.reproduciendo=0  
        self.fin_hilo = False
        signal.signal(signal.SIGINT, self.rutina_salir)
        signal.signal(signal.SIGTERM, self.rutina_salir)        
        # Thread que controla la reproduccion automatica de las canciones
        self.thread = threading.Thread(target=self.detectar_fin_cancion, args=(1,))
        self.thread.start()

    def rutina_salir(self, signum, frame):
        self.detener_cancion()
        self.fin_hilo = True
        sys.exit(0)

    def reproducir_cancion(self):
        if(self.reproduciendo==0 and len(self.songs) > 0):
            print('Iniciando reproduccion')
            self.currentSong = self.songs[self.indice]
            cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/" + GestorArchivos.DIRECTORIO_ARCHIVOS + self.currentSong
            pwd = "raspberry"
            p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
            self.reproduciendo=1
            if(self.indice==(len(self.songs)-1)):
                self.indice=0
            else:
                self.indice=self.indice+1

    def detener_cancion(self):
        if(self.reproduciendo==1):
            print('Deteniendo reproduccion')
            f = open("detenertransmision.txt", "w")
            f.write("d")
            f.close()
            while(True):
                try:
                    f = open("fintransmision.txt", "r")
                    aux=f.read()
                    f.close()
                    if(aux=="fin"):
                        break
                except Exception as e:
                    pass
            self.reproduciendo=0
            self.currentSong = ""

    def siguiente_cancion(self):
        if(self.reproduciendo==1):
            self.detener_cancion()
            self.reproducir_cancion()

    def anterior_cancion(self):
        if(self.reproduciendo == 1):
            self.detener_cancion()
            if (self.indice > 1):
                self.indice -= 2
            elif (self.indice == 1):
                self.indice = len(self.songs) - 1
            else:
                self.indice = len(self.songs) - 2
            self.reproducir_cancion()

    def actualizar_canciones(self):
        self.songs = []
        for root, folders, files in os.walk(GestorArchivos.DIRECTORIO_ARCHIVOS):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(wav)$", filename) != None:
                    self.songs.append(filename)
        self.indice=0

    def detectar_fin_cancion(self, name):
        while(not self.fin_hilo):
            #Chequear si la cancion actual termino
            if(self.reproduciendo==1):
                try:
                    f = open("fintransmision.txt", "r")
                    aux=f.read()
                    f.close()
                    if(aux=="fin"):
                        f = open("fintransmision.txt", "w")
                        f.write("-")
                        f.close()
                        #Pasar a cancion siguiente
                        self.reproduciendo = 0
                        self.reproducir_cancion()
                except Exception as e:
                    pass
            time.sleep(1)

    def estado_emisora(self):
        estados = {
           "song" : self.currentSong,
           "frequency" : self.frequency,
           "status" : self.reproduciendo
        }
        return estados
