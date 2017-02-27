"""Selfie for science.

Usage:
  run_bot.py <selfie_folder_path>
  run_bot.py (-h | --help)
  run_bot.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from PIL import Image
from io import BytesIO

import os
import requests
import settings
import sys
import telebot
import uuid
from urllib import request


bot = telebot.TeleBot(settings.API_TOKEN)
img_counter = 0


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, settings.HELP_MESSAGE)


@bot.message_handler(content_types=['document'])
def handle_doc(message):
    global img_counter
    try:
        file_info = bot.get_file(message.document.file_id)
        file_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(settings.API_TOKEN, file_info.file_path)
        img = request.urlopen(file_url).read()
    except:
        bot.send_message(message.chat.id, settings.BAD_IMAGE_MESSAGE)

    try:
        im = Image.open(BytesIO(img))
        im.verify()

        file_path = os.path.join(arguments['<selfie_folder_path>'], str(uuid.uuid4()) + '.png')
        with open(file_path, 'wb') as file:
            file.write(img)

        bot.send_message(message.chat.id, settings.THANKS_MESSAGE)
        img_counter += 1
        print('Image №:', img_counter, 'downloaded.')
    except:
        bot.send_message(message.chat.id, settings.BAD_IMAGE_MESSAGE)


@bot.message_handler(content_types=['photo', 'audio', 'video'])
def handle_doc(message):
    bot.send_message(message.chat.id, settings.NO_PHOTO_MESSAGE)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, settings.NO_PHOTO_MESSAGE)


if __name__ == '__main__':
    global arguments
    arguments = docopt(__doc__, version='Selfie for science 1.0')

    bot.polling()
