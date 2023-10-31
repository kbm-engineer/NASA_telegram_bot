
TOKEN = '6538881829:AAHyi660uSppbOwr2RKlpwqbSFnzZs-8gUA'


import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_image(earth_date, save_path):
    link = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    api_key = 'DnZoGGbzG4v2pa2rBT1NT2egAWTeSCakqjxVWvf7'
    earth_date = earth_date
    camera = 'FHAZ'

    params = {
        'api_key': api_key,
        'earth_date': earth_date,
        'camera': camera,
    }

    try:
        response = requests.get(link, params=params)
        data = response.json()
        img_src = data["photos"][0]["img_src"]
        # Скачиваем изображение
        image_data = requests.get(img_src).content
        # Сохраняем изображение в файл
        with open(save_path, 'wb') as f:
            f.write(image_data)
    except:
        img_src = '''В выбранную дату снимков с фронтальной камеры марсахода не обнаружено.
        Посмотрте соседние дни, обычно снимки доступны с шагом в одни земные сутки.'''
        print(img_src)

get_image('2023-01-01', 'mars_image.jpg')