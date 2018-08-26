from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects import mysql

from .setting import Base
from .setting import ENGINE

class AnimeList(Base):
    __tablename__ = 'anime_list'
    table_id = Column('id', Integer, primary_key = True)
    year = Column('year', mysql.YEAR)
    cour = Column('cour', Integer)
    title = Column('title', String(100))

    def __str__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.table_id)
        string += ', year:' + str(self.year)
        string += ', cour:' + str(self.cour)
        string += ', title:' + self.title
        return string
