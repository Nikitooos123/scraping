import requests
from bs4 import BeautifulSoup as bs
import json

url = 'https://www.skiddle.com/inspire-me/festivals-2023'
headres = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
    'Accept': '*/*'
}

src = requests.get(url, headers=headres)
soup = bs(src.text, 'html.parser')

items = soup.find_all('div', class_='inspire-event-block-block')
href = [i.find_all('div', class_="card flex-height lvl-1 brt-5px bg-white relative has-details ticket-button") for i in items]
list_href = ['https://www.skiddle.com' + i.find('a').get('href') for j in href for i in j]
festivals = []
data = {}
count = 1
for item in list_href:
    src = requests.get(item, headers=headres)
    soup = bs(src.text, 'html.parser')
    try:
        item_name = soup.find('div', class_='MuiBox-root css-8tc97e').find('h1').text
    except (Exception):
        print('Error no festival...')
        continue
    try:
        item_data = soup.find('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol').text
    except (AttributeError):
        item_data = soup.find('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-16jpb7r').text
    try:
        item_location = soup.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')[1].text
    except:
        item_location = soup.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-16jpb7r')[1].text
    print(f'#{count}. {item_name}...')
    count += 1
    data['Data'] = item_data
    data['Location'] = item_location
    festivals.append(
        {
            "Name_festifal": item_name,
            "Data and location": data
        }
    )

with open('skiddle_festifal.json', 'a', encoding='UTF-8') as file:
    json.dump(festivals, file, indent=4, ensure_ascii=False)
    print('Download completed!')
