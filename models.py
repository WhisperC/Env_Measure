from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from collections import OrderedDict


engine = create_engine('sqlite:///sqlalchemy.db', echo=False)
Base = declarative_base()


class SongLists(Base):
    __tablename__ = 'songlists'
    id = Column(Integer, primary_key=True)
    arg_a = Column(Integer)
    arg_b = Column(Integer)
    arg_c = Column(Integer)
    name = Column(String(200), unique=True)
    songs = relationship("Songs")


class Songs(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    arg_a = Column(Integer)
    arg_b = Column(Integer)
    arg_c = Column(Integer)
    name = Column(String(200), unique=True)
    belong_list_id = Column(Integer, ForeignKey('songlists.id'))

    belong_list = relationship("SongLists")


class Test:
    def __init__(self, arg_a, arg_b, arg_c):
        self.arg_a = arg_a
        self.arg_b = arg_b
        self.arg_c = arg_c


