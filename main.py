import telebot
from telebot import types

from config import *
from extensions import CryptoConverter, APIException            # ошибки на стороне сервера, на стороне пользователя

def create_markup(base = None):                                 # определим клавиатуру динамически (при нажатии на одну из кнопок, эта кнопка пропадает)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))   # на каждую кнопку ставим название валюты - это ключ из словаря exchanges

    markup.add(*buttons)       # добавляем все кнопки разом
    return markup

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = '/values    - список всех доступных валют \n/convert - конвертирование из <валюты> в <валюту> <в кол-ве>'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():     # пройдем по ключам списка-словаря и написать каждый ключ с новой строки
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)     # bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup())   # в параметр reply_markup передаем нашу клавиатуру
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = 'Выберите количество конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e}")
    else:
        # text = f"Цена {amount} {base} в {quote} составляет: {new_price}"
        text = f"Цена {amount} {base} в {quote} составляет: {new_price}\n/convert - Продолжить,\n/values   - список доступных валют"
        bot.send_message(message.chat.id, text)

        # source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        # # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        # source_markup_btn1 = types.KeyboardButton('ПРОДОЛЖИТЬ')
        # source_markup_btn2 = types.KeyboardButton('ХОЧУ ВЫЙТИ')
        # source_markup.add(source_markup_btn1, source_markup_btn2)
        # bot.send_message(message.chat.id, text, reply_markup=source_markup)


bot.polling()

