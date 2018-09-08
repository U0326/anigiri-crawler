import logging
import datetime

from module.twitter.search_tweet import SearchTweet
from module.twitter.search_words_taker import SearchWordsTaker
from module.db.setting import session
from module.db.search_results import SearchResult
from module.util.db.anime_list_util import AnimeListUtil

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    date = datetime.datetime.now()
    anime_list = AnimeListUtil.take_current_cour_anime_list(date)
    taker = SearchWordsTaker()
    search_tweet = SearchTweet(date)

    for anime in anime_list:
        search_words = taker.take_search_words(anime)
        total_tweet_count_per_anime = 0
        negative_tweet_count_per_anime = 0
        for word in search_words:
            total_tweet_count_per_word, negative_tweet_count_per_word = \
                    search_tweet.search_yestaday_tweet(word)
            total_tweet_count_per_anime += total_tweet_count_per_word
            negative_tweet_count_per_anime += negative_tweet_count_per_word

        try:
            search_result = SearchResult()
            search_result.anime_id = anime.row_id
            search_result.total_tweet_count = total_tweet_count_per_anime
            search_result.negative_tweet_count = negative_tweet_count_per_anime
            session.add(search_result)
        except:
            logger.exception("Registration to DB for search results is failed.")
            session.rollback()
            raise

    session.commit()

