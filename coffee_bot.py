import json
import logging
import os
import random
import time

import telebot

LIST_FILENAME = 'coffee_house_list.json'

# using get will return `None` if a key is not present rather than raise a `KeyError`
token = os.environ.get('TG_BOT_TOKEN')

bot = telebot.TeleBot(token)


def loadCoffeeHouseList():
    list = []
    with open(LIST_FILENAME) as json_file:
        data = json.load(json_file)
        for p in data['coffeehouse']:
            list.append(p['name'])
    return list


@bot.message_handler(commands=['help'])  # help command handler
def send_help(message):
    logger.info('command [help] was received')

    helpStr = 'Выбираем из [' + ', '.join(coffeeHouses) + ']'
    bot.reply_to(message, helpStr)


@bot.message_handler(content_types=['text'])  # text message handler
def send_smth(message):
    logger.info('receive message: [%s]', message)
    sendResponse(message)


@bot.message_handler(content_types=['audio', 'video', 'document', 'location', 'contact', 'sticker'])
def send_smth(message):
    logger.info('receive not text message')
    sendResponse(message)


def sendResponse(message):
    coffeeHouse = random.choice(coffeeHouses)
    rs = "Наш сегодняшний путь лежит в ...\n" + coffeeHouse
    photo = open('pic/default.png', 'rb')

    bot.send_photo(message.chat.id, photo, rs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("coffee_bot")

    coffeeHouses = loadCoffeeHouseList()

    while True:
        try:
            bot.polling(none_stop=True)
            # ConnectionError and ReadTimeout because of possible timout of the requests library
            # maybe there are others, therefore Exception
        except Exception:
            time.sleep(15)
