from sqlalchemy import Column, Integer, String, Boolean

from .setting import Base
from .setting import ENGINE

class SearchKeyword(Base):
    __tablename__ = 'search_keywords'
    row_id = Column('id', Integer, primary_key = True)
    anime_id = Column('anime_id', Integer)
    keyword = Column('keyword', String(100))
    is_hashtag = Column('is_hashtag', Boolean)

    def __repr__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.row_id)
        string += ', anime_id:' + str(self.anime_id)
        string += ', keyword:' + str(self.keyword)
        string += ', is_hashtag:' + str(self.is_hashtag)
        return string

