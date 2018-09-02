from sqlalchemy.schema import FetchedValue
from sqlalchemy import Column, Integer, DateTime

from .setting import Base

class SearchResult(Base):
    __tablename__ = 'search_results'
    table_id = Column('id', Integer, primary_key = True)
    anime_id = Column('anime_id', Integer)
    total_tweet_count = Column('total_tweet_count', Integer)
    negative_tweet_count = Column('negative_tweet_count', Integer)
    created_at = Column('created_at', DateTime, FetchedValue())

    def __repr__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.table_id)
        string += ', anime_id:' + str(self.anime_id)
        string += ', total_tweet_count:' + str(self.total_tweet_count)
        string += ', negative_tweet_count:' + str(self.negative_tweet_count)
        string += ', created_at:' + str(self.created_at)
        return string
