from enum import Enum

class Cours(Enum):
    COUR_1 = (1, range(1, 4))
    COUR_2 = (2, range(4, 7))
    COUR_3 = (3, range(7, 10))
    COUR_4 = (4, range(10, 13))

    @classmethod
    def convert_month_to_cour(self, month):
        for cour in Cours:
            if month in cour.value[1]:
                return cour.value[0]
