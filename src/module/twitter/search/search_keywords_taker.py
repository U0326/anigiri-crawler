import logging
import pprint

from ...db.setting import session
from ...db.search_keywords import SearchKeyword
from ...util.anime_cour import Cours

logger = logging.getLogger(__name__)

class SearchKeywordsTaker:
    def take_search_keywords(self, anime):
        try:
            records = session.query(SearchKeyword) \
                    .filter(SearchKeyword.anime_id == anime.row_id) \
                    .all()
            logger.debug(pprint.pformat(records))
            return records
        except:
            logger.exception("Taking search words is failed.")
            raise

