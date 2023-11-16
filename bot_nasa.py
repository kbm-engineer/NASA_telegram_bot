import os
from dotenv import load_dotenv
import logging


from telegram import Update, InputMediaPhoto
from telegram.ext import filters, ApplicationBuilder, MessageHandler, ContextTypes

import requests


load_dotenv()

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.WARNING
# )


class CustomLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования по умолчанию

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Устанавливаем уровень логирования для этого обработчика

        # Создаем форматтер для вывода
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)


class RoverNasaAPI:
    CURIOSITY = 'Curiosity'
    PERSEVERANCE = 'Perseverance'
    CAMERA = 'camera'

    ROVERS = {
        CURIOSITY: {
            CAMERA: [
                'FHAZ',
                'RHAZ',
                'MAST',
                'CHEMCAM',
                'MAHLI',
                'MARDI',
                'NAVCAM',
                ]
        }, 
        PERSEVERANCE: {
            CAMERA: [
                'FRONT_HAZCAM_LEFT_A',
                'FRONT_HAZCAM_RIGHT_A',
                'MCZ_LEFT',
                'MCZ_RIGHT',
                'NAVCAM_LEFT',
                'NAVCAM_RIGHT',
                'REAR_HAZCAM_LEFT',
                'REAR_HAZCAM_RIGHT',
                'SKYCAM',
                'SUPERCAM_RMI'
                ]
        },
    }

    def __init__(self, api_key): #update: Update
        self.api_key = api_key
        #self.update = update


    async def poll_link(self, name_rover, earth_date):
        link = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{name_rover}/photos'
        photo_list = []
        for cam in self.ROVERS.get(name_rover).get(self.CAMERA):
            params = {
                'api_key': self.api_key,
                'earth_date': earth_date,
                'camera': cam,
            }
            try:
                logger.info(f'Запрос фото на {earth_date}')
                response = requests.get(link, params=params)
                data = response.json()
                data_json = data["photos"][0]["img_src"]
                image_data = requests.get(data_json).content
                photo_list.append(InputMediaPhoto(media=image_data))
            except:
                logger.warning(f'Нет фотографий в дату запроса')
                break
        return photo_list

    async def get_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        usernam_chat = update.effective_chat.username
        earth_date = update.message.text
        logger.info(f'Поступил запрос от {usernam_chat}')

        for rover in self.ROVERS:
            await context.bot.send_message(chat_id=chat_id, text= f'Запрос фотографий с марсохода {rover}')
            photo_list = await self.poll_link(rover, earth_date)
            try:
                await context.bot.send_media_group(chat_id=chat_id, media=photo_list)
            except:
                await context.bot.send_message(chat_id=chat_id, text=f'Для "{rover}" нет фотографий')
        
        # try:
        #     await context.bot.send_message(
        #         chat_id=chat_id,
        #         text=f'Доступность камер: -----------. Загружаем сники...')
        #     await context.bot.send_media_group(chat_id=chat_id, media=photo_list)
        # except:
        #     await context.bot.send_message(chat_id=chat_id, text=f'За {earth_date} нет фотографий')


if __name__ == '__main__':
    logger = CustomLogger(__name__)
    TOKEN = os.getenv("TOKEN")
    API_KEY = os.getenv("API_KEY")
    application = ApplicationBuilder().token(TOKEN).build()
    rover = RoverNasaAPI(API_KEY)
    get_image_handler = MessageHandler(filters.ALL, rover.get_image)
    application.add_handler(get_image_handler)
    application.run_polling()