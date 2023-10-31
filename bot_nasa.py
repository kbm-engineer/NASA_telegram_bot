TOKEN = '6538881829:AAHyi660uSppbOwr2RKlpwqbSFnzZs-8gUA'


import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, ContextTypes
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я маленький бот для получения картинок с Марса. "
        "Пожалуйста, отправь мне дату в формате 'гггг-мм-дд'. Если что то епадёт не волнуйся, я только учусь."
    )


async def get_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    rover_name = [
        'curiosity',
        'perseverance',
    ]

    link = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name[1]}/photos'
    api_key = 'DnZoGGbzG4v2pa2rBT1NT2egAWTeSCakqjxVWvf7'
    earth_date = update.message.text
    # camera = [
    #     'FHAZ',
    #     'RHAZ',
    #     'MAST',
    #     'CHEMCAM',
    #     'MAHLI',
    #     'MARDI',
    #     'NAVCAM',
    #     ]
    
    camera = [
        "FRONT_HAZCAM_LEFT_A",
        "FRONT_HAZCAM_RIGHT_A",
        "MCZ_LEFT",
        "MCZ_RIGHT",
        "NAVCAM_LEFT",
        "NAVCAM_RIGHT",
        "REAR_HAZCAM_LEFT",
        "REAR_HAZCAM_RIGHT",
        "SKYCAM",
        "SUPERCAM_RMI"
        ]

    await context.bot.send_message(chat_id=chat_id, text='Секундочку...')
    photo_list = []
    for cam in camera:
        params = {
            'api_key': api_key,
            'earth_date': earth_date,
            'camera': cam,
        }

        try:
            response = requests.get(link, params=params)
            data = response.json()
            data_json = data["photos"][0]["img_src"]
            image_data = requests.get(data_json).content
            photo_list.append(InputMediaPhoto(media=image_data))
        except:
            break
    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'Доступность камер: {len(photo_list)}/{len(camera)}. Загружаем сники...')
        await context.bot.send_media_group(chat_id=chat_id, media=photo_list)
    except:
        await context.bot.send_message(chat_id=chat_id, text=f'За {earth_date} нет фотографий')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    get_image_handler = MessageHandler(filters.ALL, get_image)
    application.add_handler(start_handler)
    application.add_handler(get_image_handler)
    application.run_polling()