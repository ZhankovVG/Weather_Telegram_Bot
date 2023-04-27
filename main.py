import telebot
import requests
import json

bot = telebot.TeleBot('5951886439:AAGatqMJR0dGXOAFuloW2BSGsZd0PE-zTuc')
weather_token = '2070be680625e8d2ff928eda62414d95'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']


        
        bot.reply_to(message, f'Сейчас погода: {temp}')


    else:
        bot.reply_to(message, f'Город указан не верно')


bot.polling(non_stop=True)
