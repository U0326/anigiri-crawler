import sys
import logging
from datetime import datetime, timedelta

from module.twitter.search.search_tweet import SearchTweet
from module.twitter.search.search_keywords_taker import SearchKeywordsTaker
from module.db.setting import session
from module.db.search_results import SearchResult
from module.util.db.anime_list_util import AnimeListUtil

log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
logging.basicConfig(level = logging.INFO, format = log_format)
logger = logging.getLogger(__name__)

def isValitArgs(args):
    if len(args) == 1:
        return True
    if len(args) > 2:
        logger.error('Args are invalid. \
                Usage: search_twitter_invoker [days_ago\(default:1\)]')
        return False
    if not (args[1].isdigit() and (1 < int(args[1]) < 7)):
        logger.error('Arg is invalid. Valid value is 1 to 6.')
        return False
    return True

if __name__ == '__main__':
    logger.info('search_twitter_invoker start.')
    args = sys.argv
    if not isValitArgs(args): sys.exit()
    days_ago = args[1] if len(args) == 2 else 1
    target_date = (datetime.now() - timedelta(days =+ (int(days_ago)))).date()
    logger.debug('The search target date is ' + str(target_date))

    anime_list = AnimeListUtil.take_current_cour_anime_list(target_date)
    taker = SearchKeywordsTaker()
    search_tweet = SearchTweet(target_date)

    for anime in anime_list:
        search_keywords = taker.take_search_keywords(anime)
        sampling_tweet_count, gave_up_tweet_count = \
                search_tweet.search_tweet(search_keywords)

        try:
            search_result = SearchResult()
            search_result.anime_id = anime.row_id
            search_result.sampling_tweet_count = sampling_tweet_count
            search_result.gave_up_tweet_count = gave_up_tweet_count
            search_result.tweeted_date = target_date
            session.add(search_result)
        except:
            logger.exception('Registration to DB for search results is failed.')
            session.rollback()
            raise

    session.commit()
    logger.info('search_twitter_invoker end.')

