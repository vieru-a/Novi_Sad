"""
Парсер для сайта 4zida. Собираем данные о домах (у которых есть фото) с ценой в интервале 15.000 - 100.000.
Создаем json документ, куда добавляем: адрес, цену, площадь, кол-во комнат, описание, структуру постройки, фото
и цену за квадратный метр. При наличии у дома описания и названия структуры - переводим с сербского на русский язык.
"""

import json
import requests
# import shutil
import os

from googletrans import Translator
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


def run():
    def get_json(url):
        r = requests.get(url, headers=headers)
        src = r.json()
        return src

    translator = Translator()

    check_list = ['title', 'price', 'm2', 'roomCount', 'desc', 'structureName', 'images', 'pricePerM2']

    house_number = 1

    for i in range(1, 10):
        # получаем json страниц с домами с ценой от 15.000 до 100.000
        page = get_json(
            f'https://api.4zida.rs/v6/search/houses?for=sale&priceFrom=15000&priceTo=100000&page={i}&placeIds%5B%5D=600')

        for house in page['ads']:
            # работаем только с теми домами, у которых есть фотографии
            if 'image' in house:
                # получаем json страницы дома
                house_json = get_json('https://api.4zida.rs/v6/eds/' + house['id'])
                # создаем словарь с характеристиками дома
                house_dic = {}
                for k, v in house_json.items():
                    # нас интересуют только: адрес, цена, площадь, кол-во комнат, описание, структура, фото и цена/кв.метр
                    if k in check_list:
                        # при наличии описания и структуры переводим на русский
                        if v != '' and k in check_list[4] or k in check_list[5]:
                            house_dic[k] = translator.translate(v, dest='ru', src='sr').text
                        elif v == '':
                            house_dic[k] = 'Нет данных'
                        else:
                            house_dic[k] = v

                path = f'templates/static/assets/media/house_{house_number}'
                # создаем директорию для каждого дома
                os.mkdir(BASE_DIR / path)
                # преобразуем словарь с нужными нам данными в json и сохраняем его в созданную директорию
                with open(BASE_DIR / f'{path}/data.json', 'w', encoding='utf-8') as fp:
                    json.dump(house_dic, fp)
                    print(f'house_{house_number}.json saved')

                house_number += 1
