from enum import Enum

import datetime
import logging
import json

from ..db.setting import session
from ..db.anime_lists import AnimeList
from ..db.search_keywords import SearchKeyword
from ..util.anime_cour import Cours

import requests

logger = logging.getLogger(__name__)

class AnimeListTaker:
    END_POINT = "http://api.moemoe.tokyo/anime/v1/master"

    def __init__(self, date):
        self.date = date

    def request_corrent_cour_list(self):
        year = self.date.year
        cour = Cours.convert_month_to_cour(self.date.month)
        logger.info('In the request, the parameters year:' \
                + str(year) +' and cour:' + str(cour)  +' will send.')
        response = requests.get(AnimeListTaker.END_POINT \
                + "/" + str(year) + "/" + str(cour))
        logger.info(str(len(response.json())) + ' animations hit.')
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
        keywords = self.take_keywords_from_titles(src)
        keywords += self.take_keyword_from_hashtag(src)
        for index, keyword in enumerate(keywords):
            search_keyword = SearchKeyword()
            search_keyword.anime_id = anime.row_id
            search_keyword.keyword = keyword
            if index is len(keywords) - 1:
                search_keyword.is_hashtag = True
            else:
                search_keyword.is_hashtag = False
            session.add(search_keyword)

    def take_keywords_from_titles(self, src):
        words = list(filter(lambda str:str!= '', {src['title'], src['title_short1'], \
                src['title_short2'], src['title_short3']}))
        return self.delete_duplicate_word(words)

    def delete_duplicate_word(self, words):
        result_list = []
        for i in range(0, len(words)):
            logger.debug('search word adding candidate: ' + words[i])
            for j in range(0, len(words)):
                if i == j: continue
                logger.debug('for comparison: ' + words[j])
                # キーワード追加候補に含まれる、より短いワードが存在する場合、
                if words[i].find(words[j]) != -1:
                    logger.debug('Word is not added, Because shorter one exists.')
                    # 短い方を優先する。
                    break
            else:
                logger.debug('Word is added.')
                result_list.append(words[i])
        return result_list

    def take_keyword_from_hashtag(self, src):
        return [src['twitter_hash_tag']]
