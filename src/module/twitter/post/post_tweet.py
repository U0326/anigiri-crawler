import logging

from .twitter_config import twitter_api

logger = logging.getLogger(__name__)

class PostTweet:
    POST_URL = 'https://api.twitter.com/1.1/statuses/update.json'

    def post_tweet(self, text):
        params = {
                'status': text
                }
        try:
            response = twitter_api.post(self.POST_URL, params = params)
            response.raise_for_status()
        except:
            logger.exception('A HTTP request to post tweet is failed.')
            raise

if __name__ == '__main__':
    post_tweet = PostTweet()
    post_tweet.post_tweet('テスト投稿')
