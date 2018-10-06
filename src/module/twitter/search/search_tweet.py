import json
import logging
import time
from datetime import datetime, date, timedelta

from pytz import timezone
from dateutil import parser

from ..twitter_config import twitter_api
from ...db.search_keywords import SearchKeyword

logger = logging.getLogger(__name__)

class SearchTweet:
    SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
    TWEETS_PER_PAGE = 100
    COOLDOWN_MINUTES_OF_SEARCH = 15
    LIMITED_COUNT_OF_CONTINUOUSLY_SEARCH = 180
    search_count = 0

    def __init__(self, date):
        self.today = date
        self.yestaday = (self.today - timedelta(days=1)).date()
        # tweetの検索時にmax_idを指定することで、そのid以前のtweetのみを対象にできる。
        self.max_id = 0

    def search_yestaday_tweet(self, search_keywords):
        sampling_tweet_count = 0
        gave_up_tweet_count = 0
        for search_keyword in search_keywords:
            if search_keyword.is_hashtag:
                keyword = '#' + search_keyword.keyword
                sampling_tweet_count = self.do_search(keyword)
            else:
                keyword = search_keyword.keyword + ' 切った'
                gave_up_tweet_count += self.do_search(keyword)
        return sampling_tweet_count, gave_up_tweet_count

    def do_search(self, keyword):
        headers = {'Connection': 'close'}
        params = {
                'count'         : self.TWEETS_PER_PAGE,
                'until'         : self.yestaday.strftime('%Y-%m-%d') + '_23:59:59_JST',
                'result_type'   : 'mixed',
                'lang'          : 'ja',
                'q'             : keyword + ' exclude:retweets'
                }

        tweet_count_result = 0
        self.max_id = 0
        while True:
            if self.max_id != 0: params['max_id'] = self.max_id
            try:
                self.avoid_restriction()
                logger.debug('Search query: ' + str(params))
                response = twitter_api.get(self.SEARCH_URL, \
                        params = params, headers = headers)
                response.raise_for_status()
                timeline = json.loads(response.text)['statuses']
                logger.debug('Timeline size: ' + str(len(timeline)))
            except:
                logger.exception('A HTTP request to take tweet is failed.')
                raise
            tweet_count, is_need_next_timeline = self.parse_timeline(timeline)
            logger.info('Searching with "' + params['q'] + '", ' \
                    'coming out tweet count is "' + str(tweet_count) + '".')
            tweet_count_result += tweet_count
            if not is_need_next_timeline: break

        return tweet_count_result

    def avoid_restriction(self):
        self.search_count += 1
        if self.search_count >= self.LIMITED_COUNT_OF_CONTINUOUSLY_SEARCH:
            logger.info('Execution sleeps to avoid API restriction.')
            time.sleep(self.COOLDOWN_MINUTES_OF_SEARCH * 60)
            self.search_count = 0

    def parse_timeline(self, timeline):
        tweet_count = 0
        is_need_next_timeline = False
        for tweet in timeline:
            logger.debug('tweet id: ' + str(tweet['id']))
            logger.debug('tweet created at: ' + tweet['created_at'])
            created_date = parser.parse(tweet['created_at']) \
                    .astimezone(timezone('Asia/Tokyo')).date()
            if created_date < self.yestaday:
                if self.max_id == 0:
                    # 人気が高いツイートは作成日に関わらず、タイムラインの上位となる為、
                    # 初回のループに限りbreakを行わない。
                    continue
                break
            tweet_count += 1
        else:
            if len(timeline) == self.TWEETS_PER_PAGE:
                is_need_next_timeline = True
                self.max_id = timeline[-1]['id'] - 1

        return tweet_count, is_need_next_timeline
