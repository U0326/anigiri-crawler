import logging

from ..twitter_config import twitter_api

logger = logging.getLogger(__name__)

class PostTweet:
    POST_URL = 'https://api.twitter.com/1.1/statuses/update.json'
    MAX_TWEET_LENGTH = 140
    TWEET_SUFFIX = '(続く)...'
    TWEET_PREFIX = '...(続き)'
    HASHTAG = ' #あにぎり'

    def post_tweet(self, text):
        text_with_hashtag = text + self.HASHTAG
        if self.is_need_split(text_with_hashtag):
            self.do_post_splitted_tweet(text_with_hashtag)
        else:
            self.do_post_tweet(text_with_hashtag)

    def is_need_split(self, text):
        if len(text) > self.MAX_TWEET_LENGTH:
            return True
        return False

    def do_post_splitted_tweet(self, text):
        tweet_length = self.MAX_TWEET_LENGTH - len(self.TWEET_SUFFIX)
        self.do_post_tweet(text[0:tweet_length] + self.TWEET_SUFFIX)

        # 7文字のsuffixを挿入した後に分割を行う為、
        # ↑hashtagの途中で文字数制限になっても、hashtag全体が次のツイートとして扱われる。
        remaining_text = self.TWEET_PREFIX + text[tweet_length:len(text)]
        if self.is_need_split(remaining_text):
            self.do_post_splitted_tweet(remaining_text)
        else:
            self.do_post_tweet(remaining_text)

    def do_post_tweet(self, text):
        try:
            logger.info('Sending tweet content is "' + text + "'.")
            response = twitter_api.post(self.POST_URL, params = {'status' : text})
            response.raise_for_status()
        except:
            logger.exception('A HTTP request to post tweet is failed.')
            raise

