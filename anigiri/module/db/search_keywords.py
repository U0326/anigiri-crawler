from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects import mysql

from .setting import Base
from .setting import ENGINE

class SearchKeyword(Base):
    __tablename__ = 'search_keywords'
    table_id = Column('id', Integer, primary_key = True)
    anime_id = Column('anime_id', Integer)
    keyword = Column('keyword', String(100))

    def __repr__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.table_id)
        string += ', anime_id:' + str(self.anime_id)
        string += ', keyword:' + str(self.keyword)
        return string

