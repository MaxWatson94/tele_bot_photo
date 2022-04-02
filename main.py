from config import *
from deepface import DeepFace
import telebot
from telebot import types
import requests
from translate import Translator


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Отрпавь фото и узнай все о нем!")


@bot.message_handler(content_types=['photo', 'text'])
def handler_file(message):
    from pathlib import Path
    Path(f'files/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    bot.send_message(message.chat.id, 'Думаю, сейчас будет готово..')

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = f'files/{message.chat.id}/' + file_info.file_path.replace('photos/', '')
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    translator = Translator(to_lang="ru")


    photo = DeepFace.analyze(img_path = src, actions = ['age','emotion', 'gender', 'race'])

    get_age = 'Предполагаемый возраст: ' + str(photo.get("age"))
    get_emotion = 'Эмоция на фото: ' + translator.translate(max(photo.get('emotion'), key=photo.get('emotion').get))
    get_gender = 'Пол: ' + str(photo.get('gender'))
    get_race = 'Предполагаемая раса: ' + translator.translate(max(photo.get('race')))

    result_data = [get_emotion, get_age, get_gender, get_race]
    bot.send_message(message.chat.id, result_data[0])
    bot.send_message(message.chat.id, result_data[1])
    bot.send_message(message.chat.id, result_data[2])
    bot.send_message(message.chat.id, result_data[3])


bot.infinity_polling()

