import logging

from ..db.setting import session
from ..db.anime_lists import AnimeList
from ..db.search_keywords import SearchKeyword
from ..common.anime_cour import Cours

class SearchWordsTaker:
    def __init__(self, date):
        self.date = date

    def take_title_and_search_words(self):
        anime_list = self.take_current_cour_anime_list()
        for anime in anime_list:

    
    def take_current_cour_anime_list(self):
        return session.query(AnimeList) \
                .filter(AnimeList.year == self.date.year) \
                .filter(AnimeList.cour == Cours.convert_month_to_cour(self.date.month)) \
                .all()

    def take_search_words(self):
        # ここから再開する。

