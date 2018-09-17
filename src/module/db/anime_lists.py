from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import mysql

from .setting import Base
from .setting import ENGINE

class AnimeList(Base):
    __tablename__ = 'anime_list'
    row_id = Column('id', Integer, primary_key = True)
    year = Column('year', mysql.YEAR)
    cour = Column('cour', Integer)
    title = Column('title', String(100))

    def __repr__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.row_id)
        string += ', year:' + str(self.year)
        string += ', cour:' + str(self.cour)
        string += ', title:' + self.title
        return string

