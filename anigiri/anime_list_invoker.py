import datetime
import logging

from module.anime_list.anime_list import AnimeListTaker
from module.anime_list.anime_list import AnimeListRegister

logger = logging.getLogger(__name__)

if __name__  == '__main__':
    date = datetime.datetime.now()
    taker = AnimeListTaker(date)
    try:
        anime_list = taker.request_corrent_cour_list()
    except:
        logger.exception("A HTTP request to take anime list is failed.")
    
    register = AnimeListRegister(date, anime_list)
    try:
        register.regist()
    except:
        logger.exception("Registration to DB failed.")
