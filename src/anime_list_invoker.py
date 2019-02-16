import datetime
import logging

from module.anime_list.anime_list import AnimeListTaker
from module.anime_list.anime_list import AnimeListRegister

log_format = '%(asctime)s %(levelname)s %(name)s :%(message)s'
logging.basicConfig(level = logging.INFO, format = log_format)
logger = logging.getLogger(__name__)

if __name__  == '__main__':
    logger.info('anime_list_invoker start.')
    date = datetime.datetime.now()
    taker = AnimeListTaker(date)
    try:
        anime_list = taker.request_corrent_cour_list()
    except:
        logger.exception("A HTTP request to take anime list is failed.")
        raise
    
    register = AnimeListRegister(date, anime_list)
    try:
        register.regist()
    except:
        logger.exception("Registration to DB for anime lists is failed.")
        raise
    logger.info('anime_list_invoker end.')
