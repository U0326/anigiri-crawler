import logging
import datetime

from module.twitter.trend_analyser import TrendAnalyser

log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
logging.basicConfig(level = logging.INFO, format = log_format)

if __name__ == '__main__':
    trend_analyser = TrendAnalyser(datetime.datetime.now())
    search_results = trend_analyser.take_yestaday_search_results()
    trend_analyser.sort_in_ratio_of_negative_tweet(search_results)
        
