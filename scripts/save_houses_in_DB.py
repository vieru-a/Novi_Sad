"""
Сохраняем дом в базу данных.
"""

import json
import os
from pathlib import Path
from Novi_Sad_houses.models import House

BASE_DIR = Path(__file__).resolve().parent.parent

path = 'templates/static/assets/media'


def run():
    fields_list = ['title', 'structureName', 'roomCount', 'm2', 'price', 'pricePerM2', 'desc']
    for house in range(len(os.listdir(BASE_DIR / path))):
        # открываем json каждого дома
        with open(BASE_DIR / f'{path}/house_{house+1}/data.json') as f:
            data = json.load(f)
        # проверяем каждое поле, если оно пустое, присваиваем полю значение "Нет данных"
        for i in range(len(fields_list)):
            if fields_list[i] not in data:
                data[fields_list[i]] = 'Нет данных'
        # сохраняем дом в базу данных
        save_house_in_db = House(
                title=data['title'],
                structureName=data['structureName'],
                roomCount=data['roomCount'],
                m2=data['m2'],
                price=data['price'],
                pricePerM2=data['pricePerM2'],
                desc=data['desc']
        )
        save_house_in_db.save()

        print(f'{house+1} ' + data['title'] + ' saved')
