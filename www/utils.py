import os # operative system module

import re # regular expressions module

from json import JSONEncoder

from werkzeug.utils import secure_filename
import time

from exceptions import FileFormatNotAllowedError

from models import Song

class SongEncoder(JSONEncoder):

    def default(self, object):
        if isinstance(object, Song):
            return object.__dict__
        else:
            return JSONEncoder.default(self, object)

class RadioManager():

    UPLOAD_FOLDER = 'songs/'
    ALLOWED_EXTENSIONS = set(['mp3','wav'])

    def __init__(self):
        pass

    def get_names_songs(self):
        file_list = []
        k = 1
        for root, folders, files in os.walk(self.UPLOAD_FOLDER):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(aac|mp3|wav|flac|m4a|ogg|pls|m3u)$", filename) != None:
                    file_list.append(Song(k,filename))
                    k = k + 1
        return file_list

    def get_names_songs_json(self):
        file_list = []
        k = 1
        for root, folders, files in os.walk(self.UPLOAD_FOLDER):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(aac|mp3|wav|flac|m4a|ogg|pls|m3u)$", filename) != None:
                    file_list.append(SongEncoder().encode(Song(k,filename)))
                    k = k + 1
        return file_list

    def delete_song(self,name):
        if os.path.exists(self.UPLOAD_FOLDER+name):
          os.remove(self.UPLOAD_FOLDER+name)
          return True
        else:
          return False

    def __allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def save_song(self,file):
        file.filename = file.filename.replace(' ','')
        if file and self.__allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.UPLOAD_FOLDER, filename))
            if filename.rsplit('.', 1)[1].lower() != 'wav':
                self.__convert_to_wav(filename)
            return True
        else:
            raise FileFormatNotAllowedError("Formato de archivo no soportado")

    def __convert_to_wav(self,filename):
        print('Convirtiendo ' + filename + ' a wav...')
        nombre_wav = filename.replace('mp3','wav')
        cmd = 'sox songs/' + filename + ' -r 22050 -c 1 -b 16 -t wav songs/' + nombre_wav
        print('Ejecutando: ' + cmd)
        pwd = 'raspberry'
        # Crear un nuevo archivo .wav
        p = subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
        cmd = 'rm songs/' + filename
        # Borrar el archivo original
        p = subprocess.call('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
        print('Archivo convertido con exito')


import os
import signal
import subprocess
import threading
import sys

#reproduciendo=0

class RadioProcess(object):
    process = None
    songs = []
    indice = None
    reproduciendo = None
    currentSong = ""
    FREQUENCY = 87.5
    thread = None

    def __init__(self):
        self.fin_hilo = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.reproduciendo=0
        self.update()
        print('Creando thread...')
        self.thread = threading.Thread(target=self.listening, args=(1,))
        print('Thread ' + self.thread.name + ' creado!...')
        self.thread.start()
        #fpid=os.fork()
        #if fpid==0:
        #    self.listening()

    def exit_gracefully(self, signum, frame):
        self.fin_hilo = True
        sys.exit(0)


    def start(self):
        if(self.reproduciendo==0 and len(self.songs) > 0):
            print('Iniciando reproduccion')
            self.currentSong = self.songs[self.indice]
            cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/songs/" + self.currentSong
            pwd = "raspberry"
            p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
            self.reproduciendo=1
            if(self.indice==(len(self.songs)-1)):
                self.indice=0
            else:
                self.indice=self.indice+1

    def stop(self):
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

    def next(self):
        if(self.reproduciendo==1):
            self.stop()
            self.start()

    def prev(self):
        if(self.reproduciendo == 1):
            self.stop()
            if (self.indice > 1):
                self.indice -= 2
            elif (self.indice == 1):
                self.indice = len(self.songs) - 1
            else:
                self.indice = len(self.songs) - 2
            self.start()

    def update(self):
        self.songs = []
        for root, folders, files in os.walk("songs/"):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(wav)$", filename) != None:
                    self.songs.append(filename)
        self.indice=0

    def listening(self, name):
        print('Inicio del thread ', name)
        while(not self.fin_hilo):
            if(self.reproduciendo==1):
                print('Chequeando si la cancion actual termino')
                try:
                    f = open("fintransmision.txt", "r")
                    aux=f.read()
                    f.close()
                    if(aux=="fin"):
                        f = open("fintransmision.txt", "w")
                        f.write("-")
                        f.close()
                        print('Pasando a cancion siguiente')
                        self.reproduciendo = 0
                        self.start()
                except Exception as e:
                    pass
            time.sleep(1)

    def getState(self):
        estados = {
           "song" : self.currentSong,
           "frequency" : self.FREQUENCY,
           "status" : self.reproduciendo
        }
        return estados
