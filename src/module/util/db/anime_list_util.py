import logging
import pprint

from ..anime_cour import Cours
from ...db.setting import session
from ...db.anime_lists import AnimeList
from ...db.terms import Terms

logger = logging.getLogger(__name__)

class AnimeListUtil:
    @classmethod
    def take_current_cour_anime_list(self, date):
        try:
            result = session.query(Terms, AnimeList) \
                    .filter(Terms.row_id == AnimeList.term_id) \
                    .filter(Terms.year == date.year) \
                    .filter(Terms.cour == \
                            Cours.convert_month_to_cour(date.month)) \
                    .all()
            logger.debug(pprint.pformat(result))
            return [element[1] for element in result]
        except:
            logger.exception('The Anime list could not be retrieved.')
            raise

    @classmethod
    def take_record_by_anime_id(self, anime_id):
        try:
            return session.query(AnimeList).filter(AnimeList.row_id == anime_id).first()
        except:
            logger.exception('A record could not be retrieved by anime ID.')

