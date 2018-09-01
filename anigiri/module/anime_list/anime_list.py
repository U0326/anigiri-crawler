from enum import Enum

import datetime
import logging
import json

from ..db.setting import session
from ..db.anime_lists import AnimeList
from ..db.search_keywords import SearchKeyword
from ..common.anime_cour import Cours

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


class AnimeListRegister:
    def __init__(self, date, anime_list):
        self.date = date
        self.anime_list = anime_list

    def regist(self):
        for element in self.anime_list:
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
        words = list(filter(lambda str:str!= '', {src['title'], src['title_short1'], \
                src['title_short2'], src['title_short3']}))
        for word in self.delete_duplicate_word(words):
            search_keyword = SearchKeyword()
            search_keyword.anime_id = anime.table_id
            search_keyword.keyword = word
            session.add(search_keyword)

    def delete_duplicate_word(self, words):
        result_list = []
        for i in range(0, len(words)):
            print("i: " + words[i])
            for j in range(0, len(words)):
                if i == j: continue
                print("j: " + words[j])
                # あるワードに含まれるより短いワードがある場合、
                if words[i].find(words[j]) != -1:
                    # 短い方を優先する。
                    break
            else:
                result_list.append(words[i])
        return result_list

