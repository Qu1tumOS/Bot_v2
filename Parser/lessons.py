import datetime
from datetime import date
import logging
import requests
from bs4 import BeautifulSoup as bs
from DataBase.dao import User, Lesson



logger = logging.getLogger(__name__)


def date_in_site() -> list:
    url = 'http://raspisanie.nnst.ru/public/www/hg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    date = soup.find('li', class_='zgr').text
    
    last_update = soup.find('div', class_='ref').text[13:]
    
    date2 = datetime.date(int(date[6:10]), int(date[3:5]), int(date[:2]))

    return date2

def lessons_one_day() -> dict:

    descript = 'ПМ. ОП. ОГСЭ. ЕН. ОУД.'
    url = 'http://raspisanie.nnst.ru/public/www/hg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('tr')

    rasp = {}

    begin = 12

    for tr in data[begin:]:
        two_subgroup_para = []
        for td in tr:
            check_para = td.find('a', class_='z1')
            check_cab = td.find('a', class_='z2')
            para = check_para.text if check_para else ' - '
            cab = check_cab.text if check_cab else ' - '

            if para.split('.', 1)[0] in descript:
                para = para.split('.', 1)[1][2:]
                if para[0] == ' ':
                    para = para.replace(' ', '', 1)



            if td.get('rowspan') == '6':
                date = td.text
                rasp[date] = []

            elif td.get('class') == ['nul']:
                if td.get('colspan') == '2':
                    rasp[date].append([[para, cab], [para, cab]])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append([para, cab])
                    else:
                        two_subgroup_para.append([para, cab])
                        rasp[date].append(two_subgroup_para)

            elif td.get('class') == ['ur']:
                if td.get('colspan') == '2':
                    rasp[date].append([[para, cab], [para, cab]])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append([para, cab])
                    else:
                        two_subgroup_para.append([para, cab])
                        rasp[date].append(two_subgroup_para)

    return rasp

async def add_lessons_to_table():
    print('add')
    today = date.today()
    date_site = date_in_site()

    if today == date_site and not await Lesson.find_one_or_none(day=today):
        try:
            await Lesson.add(
                day=today,
                lessons=lessons_one_day() 
            )
        except Exception as x:
            logger.error(f'error - [{x}]')

    elif date_site > today and not await Lesson.find_one_or_none(day=today):
        # logger.info(f'added None day...')
        try:
            await Lesson.add(
                day=today
            )
        except Exception as x:
            logger.error(f'error - [{x}]')
