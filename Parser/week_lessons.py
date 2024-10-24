import requests
from bs4 import BeautifulSoup as bs
from Parser.parser import url_groups
from datetime import date, timedelta
from DataBase.dao import Lesson
import redis, json
from lexicon import lessons_call, descript
from pprint import pprint



def group_par(group: str) -> dict:
    url = 'http://raspisanie.nnst.ru/public/www/' + url_groups[group]

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('tr')
    rasp = {}

    begin = 13
    end = 104

    for tr in data[begin:end]:
        two_subgroup_para = []
        
        for td in tr:
            para = td.find('a', class_='z1').text if td.find('a', class_='z1') else ' - '
            cab = td.find('a', class_='z2').text if td.find('a', class_='z2') else ' - '
            teacher = td.find('a', class_='z3').text if td.find('a', class_='z3') else ' - '
            
            if para.split('.', 1)[0] in descript: #удаление ненужных префиксов из названий предметов
                para = para.split('.', 1)[1][2:]
                if para[0] == ' ':
                    para = para.replace(' ', '', 1)
            para = para[:-4] if para in ['Экологические основы при'] else para
                    
            info = [para, cab, teacher] # данные будут храниться в таком типе [предмет, кабинет, преподователь]
            info_for_all = [info, info]


            if td.get('rowspan') == '6': # дата пар 
                date_site: str = td.text[:-4]
                rasp[date_site] = []

            elif td.get('class') in [['nul'], ['ur']]:
                if td.get('colspan') == '2':
                    rasp[date_site].append(info_for_all)
                else:
                    two_subgroup_para.append(info)
                    if len(two_subgroup_para) == 2:
                        rasp[date_site].append(two_subgroup_para)
    return rasp


async def print_day(user, timedelta_day: int = 0, more: bool = False):
    redis_connect = redis.Redis(host='localhost')
    
    value = redis_connect.get(name=f'{str(user.group)}')
    if not value:
        redis_connect.set(
            name=f'{str(user.group)}', 
            value=json.dumps(group_par(user.group)), 
            ex=60*5
            )
        value = redis_connect.get(name=f'{str(user.group)}')
    redis_connect.close()
    
    
    lessons_list = json.loads(value)
    date_datetime = date.today() + timedelta(days=timedelta_day)
    date_in_base = await Lesson.find_one_or_none(day=date_datetime)
    date_str = f'{date_datetime:%d.%m.%Y}'
    
    week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'][date_datetime.weekday()]
    
    # 'включить после того как новый вид расписания сохранитсяс в бд'
    
    if date_datetime.weekday() != 6:
        if date_str in lessons_list:
            x = lessons_list[date_str]
        elif date_in_base:
            pprint(date_in_base.lessons)
            x = date_in_base.lessons[f'{user.group}']
        else:
            return "расписания на этот день нет"
        
        tabs = 24
        output = [f'{(date_str[:-5]).rjust(15, " ")} {week.ljust(12, " ")}'] 
        if date.today().isocalendar().week < date_datetime.isocalendar().week:
            output = [f'''{(date_str[:-5]).rjust(15, " ")} {week.ljust(12, " ")}'''] 
        for num, i in enumerate(x):
            lesson = i[user.subgroup-1][0]
            cab = i[user.subgroup-1][1]
            if len(i[user.subgroup-1]) == 3:
                teacher = i[user.subgroup][2]
            else:
                teacher = " - "
            output.append(f'{lesson.ljust(tabs, " ")} {cab}')
            if more == True:
                if teacher != ' - ':
                    output.append(f'{teacher.ljust(tabs, " ")}')
                    output.append(lessons_call[date_datetime.weekday()][num])
                output.append(f' ')

            outp = '\n'.join(output)
        return f'`{outp}`'
    return "Выходной"
        