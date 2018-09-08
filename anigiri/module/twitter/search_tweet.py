import json
import logging
import time
from datetime import datetime, date, timedelta

from pytz import timezone
from dateutil import parser

from .twitter_config import twitter_api

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SearchTweet:
    SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
    TWEETS_PER_PAGE = 100
    COOLDOWN_MINUTES_OF_SEARCH = 15
    LIMITED_COUNT_OF_CONTINUOUSLY_SEARCH = 180
    NEGATIVE_WORDS = ['切った', '辞めた', 'やめた']

    search_count = 0

    def __init__(self, date):
        self.today = date

    def search_yestaday_tweet(self, query):
        yestaday = (self.today - timedelta(days=1)).date()
        params = {
                'count'         : self.TWEETS_PER_PAGE,
                'until'         : yestaday.strftime('%Y-%m-%d') + '_23:59:59_JST',
                'result_type'   : 'mixed',
                'lang'          : 'ja',
                'q'             : query
                }

        tweet_count = 0
        negative_tweet_count = 0
        while True:
            if 'max_id' in locals() : params['max_id'] = max_id
            try:
                self.avoidLimited()
                logger.debug('Search query: ' + str(params))
                response = twitter_api.get(self.SEARCH_URL, params = params)
                response.raise_for_status()
                timeline = json.loads(response.text)['statuses']
                logger.debug('Timeline size: ' + str(len(timeline)))
            except:
                logger.exception('A HTTP request to take tweet is failed.')
                raise

            for tweet in timeline:
                logger.debug('tweet id: ' + str(tweet['id']))
                logger.debug('tweet created at: ' + tweet['created_at'])
                created_date = parser.parse(tweet['created_at']) \
                        .astimezone(timezone('Asia/Tokyo')).date()
                if created_date < yestaday:
                    if not 'max_id' in locals():
                        # 人気が高いツイートは作成日に関わらず、タイムラインの上位となる為、
                        # 最初のループに限りbreakを行わない。
                        continue
                    break
                tweet_count += 1
                for word in self.NEGATIVE_WORDS:
                    if tweet['text'].find(word) != -1:
                        negative_tweet_count += 1
                        break
            else:
                if len(timeline) == self.TWEETS_PER_PAGE:
                    max_id = timeline[-1]['id'] - 1
                    continue
            break

        logger.info('[' + params['q'] + ']で検索した結果、' \
                + str(tweet_count) + '件ヒットしました。' \
                'その内ネガティブなワードを含むものが' \
                + str(negative_tweet_count) + '件でした。')
        return tweet_count, negative_tweet_count

    def avoidLimited(self):
        self.search_count += 1
        if self.search_count >= self.LIMITED_COUNT_OF_CONTINUOUSLY_SEARCH:
            logger.info('APIの利用制限を回避する為、スリープします。')
            time.sleep(self.COOLDOWN_MINUTES_OF_SEARCH * 60)
            self.search_count = 0

