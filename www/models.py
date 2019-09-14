import datetime
import base64

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, BLOB, Date
from sqlalchemy.ext.declarative import declarative_base
from json import JSONEncoder
import json
import os
import re
music_dir = "songs/"

Base = declarative_base()

class SongEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, Song):
            return object.__dict__
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)

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

class Music():
    def __init__(self):
        pass

    def get_names_songs(self):
        file_list = []
        k = 1
        for root, folders, files in os.walk(music_dir):
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
        for root, folders, files in os.walk(music_dir):
            folders.sort()
            files.sort()
            for filename in files:
                if re.search(".(aac|mp3|wav|flac|m4a|ogg|pls|m3u)$", filename) != None:
                    file_list.append(SongEncoder().encode(Song(k,filename)))
                    k = k + 1
        return file_list

    def remove_songs(self,songs):
        pass

    def delete_song(self,name):
        if os.path.exists(music_dir+name):
          os.remove(music_dir+name)
        else:
          print("The file does not exist")

# Parte MYSQL

class Team(Base):
    __tablename__ = 'team'
    id=Column(Integer, primary_key=True)
    name=Column('name', String(32))
    logo=Column('logo', BLOB)
    id_zone=Column(Integer, ForeignKey('zone.id'))

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id'  : self.id,
           'name': self.name,
           'logo': base64.b64encode(self.logo).decode("utf-8", "ignore")
           }

class Match(Base):
    __tablename__ = 'match'
    id=Column(Integer, primary_key=True)
    date=Column('date', Date, default=datetime.datetime.utcnow)
    place=Column('place', String(32))

    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'  : self.id,
           'date': self.date,
           'place': self.place
       }

class Result(Base):
    __tablename__ = 'result'
    id=Column(Integer, primary_key=True)
    id_match=Column(Integer, ForeignKey('match.id'))
    id_team=Column(Integer, ForeignKey('team.id'))
    score=Column(Integer, default=0)

class Zone(Base):
    __tablename__ = 'zone'
    id=Column(Integer, primary_key=True)
    name=Column('name', String(4))
