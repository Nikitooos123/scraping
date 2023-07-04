import requests
from bs4 import BeautifulSoup as bs
import json
import time
def spisok():
    count = 1
    lis = []
    for number in range(0, 720, 12):
        URL_list = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={number}'
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0'
        }
        time.sleep(1)
        req = requests.get(URL_list, headers=headers)
        soup = bs(req.text, 'html.parser')
        link = soup.find_all('div', class_='bt-slide-content')
        for item in link:

            item_href = item.find('a').get('href')
            item_name = item.find('a').get('title')
            lis.append(item_href)
            print(f'{count}. {item_name}: {item_href}')
            count += 1
        # print(req.text)
    with open('bunderstag.txt', 'a') as file:
        [file.write(f'{i}\n') for i in lis]

def scraping():
    person_list = []
    count = 1
    with open('bunderstag.txt') as file:
        lines = [line.strip() for line in file.readlines()]

    for person in lines:
        q = requests.get(person)
        result = q.content
        soup = bs(result, 'html.parser')
        name = soup.find('div', class_='col-xs-8 col-md-9 bt-biografie-name').find('h3').text.strip().split(',')[0]
        profession = soup.find('div', class_='col-xs-8 col-md-9 bt-biografie-name').find('div').text.strip()
        try:
            Department = soup.find('div', class_='col-xs-12 col-md-4 bt-kontakt').find('h5').text
        except (Exception):
            Department = None
        try:
            social_media = soup.find_all('a', class_='bt-link-extern')
        except (Exception):
            social_media = None
        person_dict = {
            "Имя" : name,
            "Профессия" : profession,
            "Департамент" : Department,
        }
        for item in social_media:
            if social_media == None:
                break
            item_name = item.text.strip()
            item_href = item.get('href').strip()
            person_dict[item_name] = item_href


        person_list.append(person_dict)
        print(f'#{count}: загружаем {name}...')
        count += 1

    with open('bunderstag.json', 'a', encoding='UTF-8') as file:
        json.dump(person_list, file, indent=4, ensure_ascii=False)
    print('Загруска завершена!')


scraping()