from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import csv
import random

def selen():
    count = 1
    driver = webdriver.Chrome()
    times = 40
    for i in range(0, 25):
        driver.get(f'https://realty.ya.ru/moskva/kupit/kvartira/?page={i}&rgid=165705&sort=PRICE')
        time.sleep(times)
        times = random.randint(2, 6)
        main_page = driver.page_source

        for item in pars_href(main_page):
            print(f'Загружаем объявление номер {count}!')
            count += 1
            driver.get(item)
            pars(driver.page_source)
            time.sleep(times)
            times = random.randint(1, 15)
            driver.get(f'https://realty.ya.ru/moskva/kupit/kvartira/?page={i}&rgid=165705&sort=PRICE')




def pars_href(name):
    list_announcement = []

    soup = bs(name, 'html.parser')
    a = soup.find('div', class_='OffersSerp').find('ol').find_all('li')
    for item in a:
        try:
            item_href = 'https://realty.ya.ru' + item.find('a').get('href')
        except AttributeError:
            continue
        if len(item_href) < 50:
            list_announcement.append(item_href)

    return list_announcement

def pars(url):

    soup = bs(url, 'html.parser')

    name = soup.find('h1', class_='OfferCardSummaryInfo__header--3BPby').find('div').text[9:].capitalize()
    price = soup.find('div', class_='OfferCardBottomBlock__priceContainer--3h5AM').find('span').text
    square = soup.find('div', class_='OfferCardHighlights__featureValue--2wfJ7').text
    address = soup.find('div', class_='AddressWithGeoLinks__addressContainer--4jzfZ GeoLinks__addressGeoLinks--3UPum').text
    print(name, price)
    rep = [' ', ',', ':', '!', '.', '?']
    for item in rep:
        if item in name:
            name = name.replace(item, '_')
        if item in price:
            price = price.replace(item, '_')
        if item in square:
            square = square.replace(item, '_')
        if item in address:
            address = address.replace(item, '_')

    with open('Yandex_home.csv', 'a', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (name,
             price,
             square,
             address,
             )
        )


with open('Yandex_home.csv', 'w', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        ('Название',
         'Цена',
         'Площадь',
         'Адрес',
         )
    )

selen()
