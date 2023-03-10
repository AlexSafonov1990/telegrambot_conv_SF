import telebot
import datetime
from telebot import types
from config import TOKEN, currency_dict
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Приветствую тебя👋 Я @Conv_SF_bot и я умею конвертировать валюты💱\n'
                                      'Список доступных валют💵: /values\n'
                                      'Как работать с ботом❓: /help')


@bot.message_handler(commands=["help"])
def help(message, res=False):
    bot.send_message(message.chat.id, f'❗❗Подсказка📄❗❗:\n   Для начала работы с ботом, введите запрос в формате- \n'
                                      f'❗1-<Название конвертируемой валюты💵>\n'
                                      f'❗2-<Название валюты, в которую хотите конвертировать💵>\n'
                                      f'❗3-<Количество конвертируемой валюты💵>\n'
                                      f'    Пример(Доллар Рубль 100)\n'
                                      f'❗Название валюты вводите с заглавной буквы\n'
                                      f'    в именительном падеже и через пробел❗\n'
                                      f'❗Если вы хотите ввести не целое количество валюты,\n'
                                      f'    вводите число через "."')


@bot.message_handler(commands=["values"])
def values(message, res=False):
    text = 'Доступные валюты💵: '
    bot.send_message(message.chat.id, text)
    for key in currency_dict.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введенных параметров должно быть ТРИ\n'
                               'Пример(Доллар Рубль 100)')

        quote, base, amount = values
        text = CurrencyConverter.get_price(quote, base, amount)
    except APIException as error:
        bot.reply_to(message, f'Ошибка пользователя❗\n{error}❗')
    except Exception as error:
        bot.reply_to(message, f'Не удалось обработать команду❗\n{error}❗')
    else:
        today = datetime.date.today()
        res = f'Цена {float(amount):,.2f} {currency_dict.get(quote)} в {currency_dict.get(base)} по курсу ' \
              f'на {today.strftime("%d.%m.%Y")} года составляет: {text:,.2f} {currency_dict.get(base)}'
        bot.send_message(message.chat.id, res)


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
