import datetime
from module.twitter.search_tweet import SearchTweet

if __name__ == '__main__':
    date = datetime.datetime.now()
    search_tweet = SearchTweet(date)
    search_tweet.search_yestaday_tweet('オーバーロードⅢ')
