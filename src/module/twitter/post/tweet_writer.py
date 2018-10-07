from abc import ABCMeta, abstractmethod

class TweetWriter(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def write_tweet(self):
        pass

