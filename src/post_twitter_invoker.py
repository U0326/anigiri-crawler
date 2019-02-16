import sys
import logging
import datetime

from module.twitter.post.tweet_writer_factory import TweetWriterFactory
from module.twitter.post.post_tweet import PostTweet

logger = logging.getLogger(__name__)
log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
logging.basicConfig(level = logging.INFO, format = log_format)

if __name__ == '__main__':
    logger.info('post_twitter_invoker start.')
    args = sys.argv
    tweet_writer = TweetWriterFactory.takeWriter(args[1])
    if tweet_writer is None:
        raise ValueError
    tweet_content = tweet_writer.write_tweet()
    post_tweet = PostTweet()
    post_tweet.post_tweet(tweet_content)
    logger.info('post_twitter_invoker end.')

