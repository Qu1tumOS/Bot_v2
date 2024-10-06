import requests
import datetime
from bs4 import BeautifulSoup as bs

url_groups = dict()
group_to_group_gict = dict()
groups_list = list()

def url_groups_update():

    url = 'http://raspisanie.nnst.ru/public/www/cg.htm'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    groups = soup.find_all('a', class_='z0')

    for group in groups:
        url_groups[group.text] = group.get('href')
        group_to_group_gict[group.text] = group.text
        groups_list.append(group.text)
url_groups_update()