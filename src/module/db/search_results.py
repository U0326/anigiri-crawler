from sqlalchemy.schema import FetchedValue
from sqlalchemy import Column, Integer, Date, DateTime

from .setting import Base

class SearchResult(Base):
    __tablename__ = 'search_results'
    row_id = Column('id', Integer, primary_key = True)
    anime_id = Column('anime_id', Integer)
    sampling_tweet_count = Column('sampling_tweet_count', Integer)
    gave_up_tweet_count = Column('gave_up_tweet_count', Integer)
    tweeted_date = Column('tweeted_date', Date)
    created_at = Column('created_at', DateTime, FetchedValue())

    def __repr__(self):
        string = self.__class__.__name__
        string += ' id:' + str(self.row_id)
        string += ', anime_id:' + str(self.anime_id)
        string += ', sampling_tweet_count:' + str(self.sampling_tweet_count)
        string += ', gave_up_tweet_count:' + str(self.gave_up_tweet_count)
        string += ', tweeted_date:' + str(self.tweeted_date)
        string += ', created_at:' + str(self.created_at)
        return string
