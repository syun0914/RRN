from random import randint
from datetime import datetime as dt

finalDay = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class CenturyError(Exception):
    pass


class ChangeFunction(Exception):
    pass


class RRNDate:
    def __init__(self, *year, month=None, date=None):
        if len(year) == 0:
            y2 = randint(1950, dt.today().year)
        if len(year) == 1:
            y2 = year[0]
        if len(year) == 2:
            y2 = randint(*year)
        m = month or randint(1, 12)
        endDate = 29 if (y2%4 == 0 and m == 2) else finalDay[m-1]
        self.year = y2
        self.month = m
        self.date = date if date and date <= endDate else randint(1, endDate)

    def __str__(self):
        return f'{str(self.year)[2:]}{self.month:02}{self.date:02}'


def genderAlienCode(gender: str, alien: bool, birth: RRNDate):
    code = 0
    century = str(birth.year)[:2]

    if century == '18':
        if alien:
            raise CenturyError('1800년대 외국인의 외국인등록번호는 없습니다.')
        elif gender == 'male':
            return 9
        elif gender == 'female':
            return 0
    elif century == '19':
        code += 1
    elif century == '20':
        code += 3

    if alien:
        code += 4

    if gender == 'female':
        code += 1
    return code


def new_1975(
    birth: RRNDate=None,
    gender: bool=None,
    alien: bool=None,
    location: int=None,
    center: int=None,
    order: int=None
):
    checksum = 0
    date = birth or RRNDate(1950, 2020)

    while date.year >= 2020 and date.month >= 10:
        if birth:
            raise ChangeFunction('2020년 10월 이후 출생자는 new_2020 함수를 이용해주십시오.')
        else:
            date = RRNDate(1950, 2020)

    gaCode = genderAlienCode(gender or None, alien or None, date)
    location = location or randint(0, 99)
    center = center or randint(0, 99)
    order = order or randint(0, 9)
    backString = f'{gaCode}{location:02}{center:02}{order}'
    integers = list(map(int, str(date) + backString))
    for i, s in enumerate('234567892345'):
        checksum += integers[i]*int(s)
    checksum = (11-checksum//11)%10
    return f'{date}-{backString}{checksum}'
    

def new_2020(
    birth: RRNDate=None,
    gender: bool=None,
    alien: bool=None,
    suffix: int=None
):
    date = birth or RRNDate(2020)

    while date.year < 2020 or date.year == 2020 and date.month < 10:
        if birth:
            raise ChangeFunction('2020년 10월 이전 출생자는 new_1975 함수를 이용해주십시오.')
        else:
            date = RRNDate(2020)

    gaCode = genderAlienCode(gender or None, alien or None, date)
    suffix = suffix or randint(0, 999999)
    return f'{date}-{gaCode}{suffix:06}'