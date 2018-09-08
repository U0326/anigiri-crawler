import logging
import pprint

from ..db.setting import session
from ..db.search_keywords import SearchKeyword
from ..util.anime_cour import Cours

logger = logging.getLogger(__name__)

class SearchWordsTaker:
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

