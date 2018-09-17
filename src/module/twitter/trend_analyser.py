import logging
import pprint
from datetime import timedelta

from ..db.setting import session
from ..db.search_results import SearchResult

logger = logging.getLogger(__name__)

class TrendAnalyser:
    def __init__(self, date):
        self.today = date

    def take_yestaday_search_results(self):
        yestaday = (self.today - timedelta(days=1)).date()
        search_results = session.query(SearchResult) \
                .filter(SearchResult.created_at.like(yestaday.strftime('%Y-%m-%d') + '%')) \
                .all()
        logger.debug('yestaday search results: ' + pprint.pformat(search_results))
        return search_results

    def sort_in_ratio_of_negative_tweet(self, search_results):
        sorted_results = sorted(list(search_results), \
                key = lambda result: result.negative_tweet_count \
                / result.total_tweet_count, reverse = True)
        logger.debug('sorted yestaday search results: ' + pprint.pformat(sorted_results))
        return sorted_results


