import requests
from bs4 import BeautifulSoup as bs
import csv
import re

# URL_TEMPLATE = "https://animego.org/anime/filter/year-from-2023/apply?sort=rating&direction=desc&page=1"
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0'
}
# r = requests.get(URL_TEMPLATE, headers=headers)
# src = r.text
#
# # сохраняем в html файл
# with open('menu_list.html', 'w', encoding='UTF-8') as file:
#     file.write(src)

with open('table_anime.csv', 'w', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        ('Название',
         'Тип',
         'Студия',
         'Первоисточник',
         'Рейтинг MPAA'
         )
    )

# открываем сохраненный нами файл
with open('menu_list.html', encoding='UTF-8') as file:
    src = file.read()

soup = bs(src, 'html.parser')
count = 1
lis = soup.find_all('div', class_="h5 font-weight-normal mb-1")

for item in lis:

    if count <= 20:
        item_href = item.find('a').get('href')
        item_text = item.find('a').text

        rep = [' ', ',', ':', '!', '.', '?']
        for item in rep:
            if item in item_text:
                item_text = item_text.replace(item, '_')

        req = requests.get(item_href, headers=headers)
        src = req.text
        with open(f'data/{count}_{item_text}.html', 'w', encoding='UTF-8') as file:
            file.write(src)

        with open(f'data/{count}_{item_text}.html', encoding='UTF-8') as file:
            src = file.read()

        soup = bs(src, 'html.parser')

        Anime_name = soup.find('div', class_='anime-title').find('h1').text
        Status = soup.find(text=re.compile('Тип')).find_next().text
        try:
            Studio = soup.find(text=re.compile('Студия')).find_next().text
        except(AttributeError, IndexError):
            Studio = 'Неизвестно'
        Primary_source = soup.find(text=re.compile('Первоисточник')).find_next().text
        Rating = soup.find(text=re.compile('Рейтинг MPAA')).find_next().find_next().find_next().find_next().text

        with open('table_anime.csv', 'a', encoding='UTF-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                (Anime_name,
                 Status,
                 Studio,
                 Primary_source,
                 Rating
                 )
            )

        count += 1


#lis = soup.find('div', class_="text-gray-dark-6 small mb-2").find_parent()
# lis = soup.find('div', class_="h5 font-weight-normal mb-1")
# lis = soup.find('div', class_="media-body").find_next()
# lis = soup.find('div', class_="text-gray-dark-6 small mb-2").find_previous_sibling()
# print(lis)
# for anime in lis:
#     print(anime.text, anime.find('a').get('href'))
# vacancies_names = soup.find_all('div', class_="media-body")
# #
# for name in vacancies_names:
#     names = name.find('a')
#     print(names.text, names.get("href")) 
