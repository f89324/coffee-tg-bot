import os
import random

import telebot

# using get will return `None` if a key is not present rather than raise a `KeyError`
token = os.environ.get('TG_BOT_TOKEN')

coffeeHouseList = ["Банзай", "Живой кофе", "Starbucks", "Правда кофе", "Prime", "Продукты", "David Doner Club"]

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help'])  # help command handler
def send_help(message):
    helpStr = 'Выбираем из [' + ', '.join(coffeeHouseList) + ']'
    bot.reply_to(message, helpStr)


@bot.message_handler(content_types=['text'])  # text message handler
def send_smth(message):
    coffeeHouse = random.choice(coffeeHouseList)
    rs = "Наш сегодняшний путь лежит в ...\n" + coffeeHouse

    bot.send_message(message.chat.id, rs)


bot.polling(none_stop=True)
