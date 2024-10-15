import requests
from bs4 import BeautifulSoup as bs
from Parser.parser import url_groups
from datetime import date, timedelta
from DataBase.dao import Lesson, User
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
            check_para = td.find('a', class_='z1')
            check_cab = td.find('a', class_='z2')
            para = check_para.text if check_para else ' - '
            cab = check_cab.text if check_cab else ' - '
            del_sunday_date = None
            
            if para.split('.', 1)[0] in descript:
                para = para.split('.', 1)[1][2:]
                if para[0] == ' ':
                    para = para.replace(' ', '', 1)

            if td.get('rowspan') == '6':
                date_site = td.text[:-4]
                rasp[date_site] = []

            elif td.get('class') == ['nul']:
                if td.get('colspan') == '2':
                    rasp[date_site].append([[para, cab], [para, cab]])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append([para, cab])
                    else:
                        two_subgroup_para.append([para, cab])
                        rasp[date_site].append(two_subgroup_para)

            elif td.get('class') == ['ur']:
                if td.get('colspan') == '2':
                    rasp[date_site].append([[para, cab], [para, cab]])
                else:
                    if not two_subgroup_para:
                        two_subgroup_para.append([para, cab])
                    else:
                        two_subgroup_para.append([para, cab])
                        rasp[date_site].append(two_subgroup_para)

    return rasp


async def print_day(user, timedelta_day: int = 0):
    date_datetime = date.today() + timedelta(days=timedelta_day)
    date_in_base = await Lesson.find_one_or_none(day=date_datetime)
    date_str = f'{date_datetime:%d.%m.%Y}'
    lessons_list = group_par(user.group)
    pprint(lessons_list)
    
    weeks_day = ['пн',
                 'вт',
                 'ср',
                 'чт',
                 'пт',
                 'сб']
     
        
    if date_str in lessons_list:
        week = weeks_day[date_datetime.weekday()]
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