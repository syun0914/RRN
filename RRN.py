from random import randint
from datetime import datetime as dt

finalDay = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class CenturyError(Exception):
    pass

class ChangeFunction(Exception):
    pass


class randomDate:
    def __init__(self, *y, m=None, d=None):
        match len(y):
            case 0: y2 = randint(1950, dt.today().year)
            case 1: y2 = y[0]
            case 2: y2 = randint(y[0], y[1])
        m = m or randint(1, 12)
        endDay = 29 if (y2%4 == 0 and m == 2) else finalDay[m-1]
        self.y, self.m = y2, m
        self.d = d if d and d <= endDay else randint(1, endDay)

    def __str__(self):
        l = list(map(lambda i: str(i).zfill(2), [self.m, self.d]))
        return ''.join([str(self.y)[2:]]+l)


def sexAlianCode(s, a, y):
    c = 0
    match str(y)[:2]:
        case '18':
            if a: raise CenturyError('1800년대 외국인의 주민등록번호는 없습니다.')
            if s: return 9
            else: return 0
        case '19': c += 1
        case '20': c += 3
    if a: c += 4
    if s: c += 1
    return c


def helpLocalCode():
    print('''
지역번호 도움말

 - 서울특별시: 00~08
 - 부산광역시: 09~12
 - 인천광역시: 13~15
 - 경기도: 16~25
 - 강원도: 26~34
 - 충청북도: 35~39
 - 대전광역시: 40~41
 - 충청남도: 42~43, 45~47
 - 세종특별자치시: 44, 96
 - 전라북도: 48~54
 - 전라남도: 55~64
 - 광주광역시: (구)55, 56 (신)65, 66
 - 대구광역시: 67~69
 - 경상북도: 70~81
 - 경상남도: 82~84, 86~91
 - 울산광역시: 85, 90
 - 제주특별자치도: 92~95
''')


def new_1975(date=None, sex=None, alian=None, loc=None):
    date = date or randomDate(1950, 2019)
    if date.y >= 2020 and date.m >= 10: raise ChangeFunction('2020년 10월 출생자부터는 new_2020 함수를 이용해주십시오.')
    saCode = sexAlianCode(sex or 0, alian or 0, date.y)
    loc = loc or randint(0, 99)
    center_order = randint(0, 999)
    endStr = str(saCode)+str(loc).zfill(2)+str(center_order).zfill(3)
    r = list(map(int, str(date)+endStr))
    iFinal = (11-(2*r[0]+3*r[1]+4*r[2]+5*r[3]+6*r[4]+7*r[5]+8*r[6]+9*r[7]+2*r[8]+3*r[9]+4*r[10]+5*r[11])//11)%10
    return str(date)+'-'+endStr+str(iFinal)
    

def new_2020(date=None, sex=None, alian=None):
    date = date or randomDate(2021, dt.today().year)
    if date.y < 2020 or (date.y==2020 and date.m < 10): raise ChangeFunction('2020년 10월 출생자부터는 new_2020 함수를 이용해주십시오.')
    saCode = sexAlianCode(sex or 0, alian or 0, date.y)
    rCode = randint(0, 999999)
    sBack = str(saCode)+str(rCode).zfill(6)
    r = list(map(int, str(date)+sBack))
    iFinal = (11-(2*r[0]+3*r[1]+4*r[2]+5*r[3]+6*r[4]+7*r[5]+8*r[6]+9*r[7]+2*r[8]+3*r[9]+4*r[10]+5*r[11])//11)%10
    return str(date)+'-'+sBack+str(iFinal)


def check(r):
    splited = r.split('-')
    if len(r) != 14 or len(splited[0]) != 6 or len(splited[1]) != 7:
        return '주민등록번호는 000000-0000000 형식의 14자리입니다.'
    t = list(map(int, r[:6]+r[7:]))
    if r[-1] != (11-(2*t[0]+3*t[1]+4*t[2]+5*t[3]+6*t[4]+7*t[5]+8*t[6]+9*t[7]+2*t[8]+3*t[9]+4*t[10]+5*t[11])//11)%10:
        return '주민등록번호의 검증 번호가 틀렸습니다.'
