import requests
from bs4 import BeautifulSoup
import json
import csv

'''сохраняем страницу файла в HTML файл'''
# URL_TEMPLATE = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0'
}
# r = requests.get(URL_TEMPLATE, headers=headers)
# # soup = bs(r.text, "html.parser")
# src = r.text
# print(src)
#
# with open('health.html', 'w', encoding='UTF-8') as file:
#     file.write(src)
'''загружаем в json файл'''
# with open('health.html', encoding='UTF-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'html.parser')
# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_text] = item_href
#
# with open('all_categories_dict.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итерации: {iteration_count}')
for categorie_name, categorie_href in all_categories.items():
    rep = [',', ' ', '-', '`']
    if count >= 0:
        for item in rep:
            if item in categorie_name:
                categorie_name = categorie_name.replace(item, '_')
        # print(categorie_name)

        req = requests.get(url=categorie_href, headers=headers)
        src = req.text

        with open(f'data/{count}_{categorie_name}.html', 'w', encoding='UTF-8') as file:
            file.write(src)

        with open(f'data/{count}_{categorie_name}.html', encoding='UTF-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')

        alert_block = soup.find(class_='uk-alert-danger')
        print(alert_block, '=========')
        if alert_block is not None:
            continue

        # cобираем заголовки таблици
        table_find = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
        product = table_find[0].text
        calories = table_find[1].text
        squirrels = table_find[2].text
        fats = table_find[3].text
        carbohydrates = table_find[4].text

        with open(f'data/{count}_{categorie_name}.csv', 'w', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (product,
                 calories,
                 squirrels,
                 fats,
                 carbohydrates)
            )
        product_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

        product_info = []
        for item in product_data:
            product_tds = item.find_all('td')

            title = product_tds[0].find('a').text
            calories = product_tds[1].text
            squirrels = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text

            product_info.append(
                {
                    'Продукт' : title,
                    'Каллорийность' : calories,
                    'Белки' : squirrels,
                    'Жиры' : fats,
                    'Углеводы' : carbohydrates
                }
            )

            with open(f'data/{count}_{categorie_name}.json', 'a', encoding='UTF-8') as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)

            with open(f'data/{count}_{categorie_name}.csv', 'a', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (title,
                     calories,
                     squirrels,
                     fats,
                     carbohydrates)
                )
        count += 1
        print(f'Итерация {count}. {categorie_name} записан...')
        iteration_count -= 1
        print(f'Итераций осталось: {iteration_count}')