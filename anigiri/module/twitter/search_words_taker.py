import logging
import pprint

from ..db.setting import session
from ..db.anime_lists import AnimeList
from ..db.search_keywords import SearchKeyword
from ..util.anime_cour import Cours

logger = logging.getLogger(__name__)

class SearchWordsTaker:
    def __init__(self, date):
        self.date = date

    def take_current_cour_anime_list(self):
        try:
            anime_list =  session.query(AnimeList) \
                    .filter(AnimeList.year == self.date.year) \
                    .filter(AnimeList.cour == \
                            Cours.convert_month_to_cour(self.date.month)) \
                    .all()
            logger.debug(pprint.pformat(anime_list))
            return anime_list
        except:
            logger.exception("Taking anime list is failed.")
            raise

    def take_search_words(self, anime):
        try:
            keyword_records = session.query(SearchKeyword.keyword) \
                    .filter(SearchKeyword.anime_id == anime.row_id) \
                    .all()
            logger.debug(pprint.pformat(keyword_records))
            return list(map(lambda record:record.keyword, keyword_records))
        except:
            logger.exception("Taking search words is failed.")
            raise

