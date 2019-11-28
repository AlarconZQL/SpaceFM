from json import JSONEncoder
from models import Song

class SongEncoder(JSONEncoder):

    def default(self, object):
        if isinstance(object, Song):
            return object.__dict__
        else:
            return JSONEncoder.default(self, object)
