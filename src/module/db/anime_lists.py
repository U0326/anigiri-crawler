from sqlalchemy import Column, Integer, String

from .setting import Base
from .setting import ENGINE

class AnimeList(Base):
    __tablename__ = 'anime_list'
    row_id = Column('id', Integer, primary_key = True)
    term_id = Column('term_id', Integer)
    title = Column('title', String(100))

    def __repr__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.row_id)
        string += ', term_id:' + str(self.term_id)
        string += ', title:' + self.title
        return string

