# Todavia no se utiliza, pero pretendemos contar con una conexion a una base de datos en el futuro.

from models import Match
from models import Result
from models import Team

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import json
import os

class Database(object):
    
    db_user = os.getenv("DB_USER") if os.getenv("DB_USER") != None else "example"
    db_pass = os.getenv("DB_PASS") if os.getenv("DB_PASS") != None else "example"
    db_host = os.getenv("DB_HOST") if os.getenv("DB_HOST") != None else "db"
    db_name = os.getenv("DB_NAME") if os.getenv("DB_NAME") != None else "tp2"
    db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") != None else "3306"


    def get_session(self):
        """Return new session

        Returns:
            [Session] -- [Return a new session]
        """
        
        connection = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (self.db_user,self.db_pass,self.db_host,self.db_port,self.db_name)
        engine = create_engine(connection)
        connection = engine.connect()
        Session = sessionmaker(bind=engine)        
        session = Session()
        return session

    def init_match(self, dict_match):
        """Generate the match in the database
    
        Returns:
            [id of match] -- [generate the two results and the match]
        """
        session = self.get_session()
        match = Match(place=dict_match["place"])
        session.add(match)
        session.commit()
        match_id = int(match.id)
        r1 = Result(id_match=match.id,id_team=dict_match["team1"])
        r2 = Result(id_match=match.id,id_team=dict_match["team2"])
        session.add(r1)
        session.add(r2)
        session.commit()
        session.close()     
        return match_id
    
    def get_all_zone_teams(self, zone):
        """Return all teams from a specific zone
        
        Arguments:
            zone {[int]} -- [The zone. 1 is for WEST | 2 is for EAST]
        
        Returns:
            [array] -- [return a array with the id, name and logo of the teams ]
        """
        session = self.get_session()
        result = session.query(Team).filter_by(id_zone = zone)
        session.close()
        return [r.serialize() for r in result]
        
    def get_match(self, id_match):
        session = self.get_session()
        match = session.query(Match).filter_by(id=id_match)
        session.close()
        return match[0].serialize()

    def get_result_match(self, id_match):
        session = self.get_session()
        results = session.query(Result).filter_by(id_match=id_match)
        session.close()
        result_match = [{
            'id_team': results[0].id_team,
            'score': results[0].score
        },{
            'id_team': results[1].id_team,
            'score': results[1].score
        }]        
        return result_match

    def get_team(self, id_team):
        session = self.get_session()
        team = session .query(Team).filter_by(id=id_team)
        session .close()
        return team[0].serialize()
    