import logging
import pprint

from ..anime_cour import Cours
from ...db.setting import session
from ...db.anime_lists import AnimeList

logger = logging.getLogger(__name__)

class AnimeListUtil:
    @classmethod
    def take_current_cour_anime_list(self, date):
        try:
            anime_list =  session.query(AnimeList) \
                    .filter(AnimeList.year == date.year) \
                    .filter(AnimeList.cour == \
                            Cours.convert_month_to_cour(date.month)) \
                    .all()
            logger.debug(pprint.pformat(anime_list))
            return anime_list
        except:
            logger.exception("Taking anime list is failed.")
            raise
