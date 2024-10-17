import logging, requests
from datetime import date
from bs4 import BeautifulSoup as bs
from DataBase.dao import Lesson
from Parser.week_lessons import group_par



logger = logging.getLogger(__name__)


def date_in_site() -> list:
    url = 'http://raspisanie.nnst.ru/public/www/hg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    date = soup.find('li', class_='zgr').text
    
    # last_update = soup.find('div', class_='ref').text[13:]
    date2 = date(int(date[6:10]), int(date[3:5]), int(date[:2]))

    return date2


async def add_lessons_to_table():
    today = date.today()
    date_site = date_in_site()

    if today == date_site and not await Lesson.find_one_or_none(day=today):
        await Lesson.add(
            day=today,
            lessons=group_par() 
        )

    elif date_site > today and not await Lesson.find_one_or_none(day=today):
        await Lesson.add(
            day=today
        )