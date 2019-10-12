import datetime
import base64

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, BLOB, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelo de un archivo de audio
class Song():

    def __init__(self,id,name):
        self.id=id
        self.name=name

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id'  : self.id,
           'name': self.name
           }