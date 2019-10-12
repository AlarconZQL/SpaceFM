import os # operative system module

import re # regular expressions module

from json import JSONEncoder

from werkzeug.utils import secure_filename

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