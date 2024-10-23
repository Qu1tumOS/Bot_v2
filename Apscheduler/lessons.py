import datetime
from datetime import date
import logging
import requests
from bs4 import BeautifulSoup as bs
from DataBase.dao import User, Lesson
from lexicon import descript



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
    url = 'http://raspisanie.nnst.ru/public/www/hg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('tr')

    rasp = {}

    begin = 12

    for tr in data[begin:]:
        two_subgroup_para = []
        for td in tr:
            para = td.find('a', class_='z1').text if td.find('a', class_='z1') else ' - '
            cab = td.find('a', class_='z2').text if td.find('a', class_='z2') else ' - '
            teacher = td.find('a', class_='z3').text if td.find('a', class_='z3') else ' - '

            if para.split('.', 1)[0] in descript:
                para = para.split('.', 1)[1][2:]
                if para[0] == ' ':
                    para = para.replace(' ', '', 1)
            para = para[:-4] if para in ['Экологические основы при'] else para
                    
            info = [para, cab, teacher] # данные будут храниться в таком типе [предмет, кабинет, преподователь]
            info_for_all = [info, info]


            if td.get('rowspan') == '6':
                date = td.text
                rasp[date] = []

            elif td.get('class') in [['nul'], ['ur']]:
                if td.get('colspan') == '2':
                    rasp[date].append([info_for_all])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append(info)
                    else:
                        two_subgroup_para.append(info)
                        rasp[date].append(two_subgroup_para)
    return rasp

async def add_lessons_to_table():
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
        try:
            await Lesson.add(
                day=today
            )
        except Exception as x:
            logger.error(f'error - [{x}]')
