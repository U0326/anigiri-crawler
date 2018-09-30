import logging
import datetime

from module.twitter.search_tweet import SearchTweet
from module.twitter.search_keywords_taker import SearchKeywordsTaker
from module.db.setting import session
from module.db.search_results import SearchResult
from module.util.db.anime_list_util import AnimeListUtil

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    date = datetime.datetime.now()
    anime_list = AnimeListUtil.take_current_cour_anime_list(date)
    taker = SearchKeywordsTaker()
    search_tweet = SearchTweet(date)

    for anime in anime_list:
        search_keywords = taker.take_search_keywords(anime)
        sampling_tweet_count, gave_up_tweet_count = \
                search_tweet.search_yestaday_tweet(search_keywords)

        try:
            search_result = SearchResult()
            search_result.anime_id = anime.row_id
            search_result.sampling_tweet_count = sampling_tweet_count
            search_result.gave_up_tweet_count = gave_up_tweet_count
            session.add(search_result)
        except:
            logger.exception("Registration to DB for search results is failed.")
            session.rollback()
            raise

    session.commit()

