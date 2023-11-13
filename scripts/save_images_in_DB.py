"""
Сохраняем фотографии для домов в базу данных.
"""

import json
import os
import requests

from pathlib import Path
from Novi_Sad_houses.models import *

BASE_DIR = Path(__file__).resolve().parent.parent

path = 'templates/static/assets/media'


def run():
    for house in range(len(os.listdir(BASE_DIR / path))):
        # открываем json каждого дома
        with open(BASE_DIR / f'{path}/house_{house+1}/data.json') as f:
            data = json.load(f)

        number = 1
        # Фото со статусом True будет главным у дома. Именно оно будет представлять дом на странице с другими домами
        default_status = True
        # получаем из базы данных дом, чтобы связать с ним фотографии
        house_from_db = House.objects.get(pk=house + 1)

        for i in data['images']:
            image_url = i['adDetails']['1920x1080_fit_0_jpeg']
            image_data = requests.get(image_url).content
            # если в директории дома уже есть фото с таким названием, добавляем к названию число
            if os.path.exists(BASE_DIR / f'{path}/house_{house+1}/1920x1080_fit_0_{number}.jpg'):
                number += 1
            # сохраняем фото в директорию с json файлом этого дома
            with open(BASE_DIR / f'{path}/house_{house+1}/1920x1080_fit_0_{number}.jpg', 'wb') as f:
                f.write(image_data)
            # сохраняем фотографию в базу данных, связываем фотографию с домом
            house_image = HouseImage(
                name=f'{number}',
                house=house_from_db,
                image=f'{house_from_db.slug}/1920x1080_fit_0_{number}.jpg',
                default=default_status
            )
            house_image.save()
            default_status = False
            print(f'{house+1} - {house_image.house.title} - {number} saved - {image_url}')
        # меняем название директории, в которой сохранены json и фото дома, на слаг дома
        os.rename(BASE_DIR / f'{path}/house_{house + 1}',
                  BASE_DIR / f'{path}/{house_from_db.slug}')
