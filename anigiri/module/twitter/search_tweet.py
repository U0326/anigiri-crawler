import json
import logging
from datetime import datetime, date, timedelta

from .twitter_config import twitter_api

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SearchTweet:
    SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
    TWEETS_PER_PAGE = 50
    NEGATIVE_WORDS = ['切った', '辞めた', 'やめた']

    def __init__(self, date):
        self.today = date

    def search_yestaday_tweet(self, query):
        # today = datetime.today()
        yestaday = (self.today - timedelta(days=1)).date()

        params = {
                'count' : self.TWEETS_PER_PAGE,
                'until': self.today.strftime('%Y-%m-%d'),
                'q' : query
                }

        tweet_count = 0
        negative_tweet_count = 0
        while True:
            if 'max_id' in locals() : params['max_id'] = max_id
            try:
                response = twitter_api.get(self.SEARCH_URL, params = params)
                response.raise_for_status()
                timeline = json.loads(response.text)['statuses']
            except:
                logger.exception('A HTTP request to take tweet is failed.')
                raise

            for tweet in timeline:
                logger.debug('tweet id: ' + str(tweet['id']))
                logger.debug('tweet created at: ' + tweet['created_at'])
                created_date = datetime.strptime(tweet['created_at'], \
                        '%a %b %d %H:%M:%S %z %Y').date()
                if created_date < yestaday: break
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


if __name__ == '__main__':
    search_tweet = SearchTweet()
    search_tweet.search_yestaday_tweet('オーバーロードⅢ')
