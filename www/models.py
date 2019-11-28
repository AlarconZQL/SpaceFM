import datetime
import base64

# Modelo de un archivo de audio
class Song():

    def __init__(self,id,name):
        self.id=id
        self.name=name

    def serialize(self):
        return {
           'id'  : self.id,
           'name': self.name
           }
