import telebot
from config import keys, TOKEN
from extensions import ConvertingException, Converter
bot = telebot.TeleBot(TOKEN)


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start", "help"])
def helps(m: telebot.types.Message):
    text = f'Добрый день, {m.chat.username}\
\nЧтобы узнать стоимость валюты напишите сообщение в виде:\
\n<имя_валюты_1> <имя_валюты_2> <кол-во_первой_валюты>.\
\n \
\nЯ понимаю названия валют на русском языке\
\nСейчас я умею работать с этими валютами - /values\
\n \
\nПример:\
\nдоллар евро 66'
    bot.reply_to(m, text)


# Функция, обрабатывающая команду /money
@bot.message_handler(commands=["values"])
def helps(m: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n' .join((text, key))
    bot.reply_to(m, text)


# Получение сообщений от юзера на обмен
@bot.message_handler(content_types=["text", ])
def handle_text(m: telebot.types.Message):
    try:
        values = m.text.split(' ')

        if len(values) != 3:
            raise ConvertingException('Ошибка в написании команды :(')

        quote, base, amount = values
        total = Converter.convert(quote, base, amount)
    except ConvertingException as e:
        bot.reply_to(m, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(m, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} - {total} {keys[base]}'
        bot.send_message(m.chat.id, text)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
