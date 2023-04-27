import requests
import json
import datetime
from config import weather_token, bot
import telebot


bot = telebot.TeleBot('5951886439:AAGatqMJR0dGXOAFuloW2BSGsZd0PE-zTuc')
weather_token = '2070be680625e8d2ff928eda62414d95'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши мне название города и я пришлю сводку погоды')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)

        city = data['name']
        temperature = data['main']['temp']
        
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['main']['temp']
        sunries_timestamp = datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(
            data['sys']['sunset'])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])
        
        

        bot.reply_to(message,
                     f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
                     f'Погода в городе: {city}\nТемпература: {temperature} C°\n'
                     f'Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м.с\n'
                     f'Восход солнца: {sunries_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {lenght_of_the_day}\n'
                     f'***Хорошего вам дня!***'
                     )

    else:
        bot.reply_to(message, f'Город указан не верно')


bot.polling(non_stop=True)
