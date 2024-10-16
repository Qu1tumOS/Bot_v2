import requests
from bs4 import BeautifulSoup as bs
from Parser.parser import url_groups
from datetime import date, timedelta
from DataBase.dao import Lesson
from pprint import pprint




def group_par(group: str) -> dict:
    descript = 'ПМ. ОП. ОГСЭ. ЕН. ОУД.'
    url = 'http://raspisanie.nnst.ru/public/www/' + url_groups[group]

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    data = soup.find_all('tr')

    rasp = {}

    begin = 13
    end = 62

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
                    
            info = [para, cab, teacher]
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


async def print_day(user, timedelta_day: int = 0):
    date_datetime = date.today() + timedelta(days=timedelta_day)
    date_in_base = await Lesson.find_one_or_none(day=date_datetime)
    date_str = f'{date_datetime:%d.%m.%Y}'
    lessons_list = group_par(user.group)
    pprint(lessons_list)
    
    week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'][date_datetime.weekday()]
     
        
    if date_str in lessons_list:
        tabs = 24
        output = [f'{date_str[:-5].rjust(15, " ")} {week.ljust(tabs-12, " ")}']
        
        for i in lessons_list[date_str ]:
            lesson = i[user.subgroup-1][0]
            cab = i[user.subgroup-1][1]
            
            output.append(f'{lesson.ljust(tabs, " ")} {cab}')

            outp = '\n'.join(output)
        return f'`{outp}`'
        
    
    if date_in_base:
        return 'дата есть в базе'
    
    else:
        return 'расписания на эту дату нет'