#HOLA FEDE

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
    ALLOWED_EXTENSIONS = set(['mp3','wav','aac','flac','m4a','ogg','pls','m3u'])

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
        if file and self.__allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.UPLOAD_FOLDER, filename))
            return True
        else:
            raise FileFormatNotAllowedError("Formato de archivo no soportado")



import os
import signal
import subprocess

#reproduciendo=0

class RadioProcess(object):
    process = None

    def __init__(self):
        self.songs = []
        for root, folders, files in os.walk("songs/"):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(wav)$", filename) != None:
                    self.songs.append(filename)

        self.indice=0
        self.reproduciendo=0
        fpid=os.fork()
        if fpid==0:
            self.listening()

    def start(self):
        if(self.reproduciendo==0):
            cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/songs/"+self.songs[self.indice]
            pwd = "raspberry"
            p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
            self.reproduciendo=1
            if(self.indice==(len(self.songs)-1)):
                self.indice=0
            else:
                self.indice=self.indice+1


    def stop(self):
        if(self.reproduciendo==1):
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

    def next(self):
        if(self.reproduciendo==1):
            self.stop()
            self.start()

    def listening(self):
        while(True):
            if(self.reproduciendo==1):
                try:
                    f = open("fintransmision.txt", "r")
                    aux=f.read()
                    f.close()
                    if(aux=="fin"):
                        f = open("fintransmision.txt", "w")
                        f.write("-")
                        f.close()
                        self.start()
                except Exception as e:
                    pass
            time.sleep(1)



    def getState(self):
        if(self.process != None):
            return "emiting"
        else:
            return "offline"
