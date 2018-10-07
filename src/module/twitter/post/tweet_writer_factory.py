from abc import ABCMeta, abstractmethod
from enum import Enum

from .daily_gave_up_tweet_writer import DailyGaveUpTweetWriter

class TweetWriterFactory(Enum):
    # コマンドライン引数, インスタンス生成のメソッドの順に設定する。
    DAILY_GAVE_UP_TWEET_WRITER = ('daily_gave_up_tweet_writer',
            DailyGaveUpTweetWriter.build)

    @classmethod
    def takeWriter(self, writer_name):
        for writer in TweetWriterFactory:
            if writer_name in writer.value[0]:
                return writer.value[1]()

