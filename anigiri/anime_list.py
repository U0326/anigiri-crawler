from enum import Enum

import datetime
import logging
import json

from db.setting import session
from db.anime_lists import AnimeList
from db.search_keywords import SearchKeyword

import requests

logger = logging.getLogger(__name__)

class AnimeListTaker:
    END_POINT = "http://api.moemoe.tokyo/anime/v1/master"

    def __init__(self, date):
        self.date = date

    def request_corrent_cour_list(self):
        response = requests.get(
                AnimeListTaker.END_POINT \
                + "/" + str(self.date.year) \
                + "/" + str(Cours.convert_month_to_cour(self.date.month)))
        response.raise_for_status()
        return response.json()


class Cours(Enum):
    COUR_1 = (1, range(1, 3))
    COUR_2 = (2, range(4, 6))
    COUR_3 = (3, range(7, 9))
    COUR_4 = (4, range(10, 12))

    @classmethod
    def convert_month_to_cour(self, month):
        for cour in Cours:
            if month in cour.value[1]:
                return cour.value[0]


class AnimeListRegister:
    def __init__(self, date, anime_list):
        self.date = date
        self.anime_list = anime_list

    def regist(self):
        for element in anime_list:
            try:
                if self.select_anime_with_title(element['title']): continue
                self.regist_anime_list(element)
                self.regist_search_keywords(element)
                session.commit()
            except:
                session.rollback()
                raise

    def regist_anime_list(self, src):
        anime = AnimeList()
        anime.year = self.date.year
        anime.cour = Cours.convert_month_to_cour(self.date.month)
        anime.title = src['title']
        session.add(anime)

    def select_anime_with_title(self, title):
        anime = session.query(AnimeList) \
                .filter(AnimeList.title == title) \
                .first()
        logger.debug(str(anime))
        return anime

    def regist_search_keywords(self, src):
        anime = self.select_anime_with_title(src['title'])
        words = set([src['title'], src['title_short1'], \
                src['title_short2'], src['title_short3']])
        for word in words:
            if not word: continue
            search_keyword = SearchKeyword()
            search_keyword.anime_id = anime.table_id
            search_keyword.keyword = word
            session.add(search_keyword)

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
