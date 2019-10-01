import datetime
import base64

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, BLOB, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
