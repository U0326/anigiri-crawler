import logging
import pprint
from datetime import datetime, timedelta

from .tweet_writer import TweetWriter
from ...db.setting import session
from ...db.search_results import SearchResult
from ...util.db.anime_list_util import AnimeListUtil

logger = logging.getLogger(__name__)

class DailyGaveUpTweetWriter(TweetWriter):
    @classmethod
    def build(self):
        return DailyGaveUpTweetWriter(datetime.now())

    def __init__(self, date):
        self.today = date

    def write_tweet(self):
        search_results = self.take_yestaday_search_results()
        sorted_search_results = self.sort_in_ratio_of_negative_tweet(search_results)
        text = '昨日最も"切られた"アニメはこれだ...' + \
                '(算出方法："切った"/公式ハッシュタグ) '
        for index, result in enumerate( sorted_search_results):
            if result.gave_up_tweet_count == 0:
                break
            # 5位までを出力する。
            if index > 4:
                break
            anime = AnimeListUtil.take_record_by_anime_id(result.anime_id)
            title = anime.title
            text += str(index + 1) + '位：「' + title + '」(' + \
                    str(result.gave_up_tweet_count) + 'ツイート/' + \
                    str(result.sampling_tweet_count) + 'ツイート)'
            # 区切り文字の挿入
            if index <= 3: text += ', '
        return text

    def take_yestaday_search_results(self):
        yestaday = (self.today - timedelta(days=1)).date()
        yestaday_search_results = session.query(SearchResult) \
                .filter(SearchResult.tweeted_date == (yestaday.strftime('%Y-%m-%d'))) \
                .all()
        logger.debug('yestaday search results: ' + pprint.pformat(yestaday_search_results))
        return yestaday_search_results

    def sort_in_ratio_of_negative_tweet(self, search_results):
        sorted_results = sorted(list(search_results), \
                key = lambda result: result.gave_up_tweet_count \
                / result.sampling_tweet_count, reverse = True)
        logger.debug('sorted yestaday search results: ' + pprint.pformat(sorted_results))
        return sorted_results

