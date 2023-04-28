import requests
import json
import datetime
from config import weather_token, bot
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot('5951886439:AAGatqMJR0dGXOAFuloW2BSGsZd0PE-zTuc')
weather_token = '2070be680625e8d2ff928eda62414d95'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 'Привет! Напиши мне название города и я пришлю сводку погоды')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    try:
        res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')
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

        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(
            text="Прогноз на 2 дня", callback_data=f"forecast_2_days_{city}")
        keyboard.add(button)

        bot.reply_to(message,
                     f'<b>Сегодня:</b> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                     f'<i>Погода в городе:</i> <b>{city}</b>\n<i>Температура:</i> {temperature} C°\n'
                     f'<i>Влажность</i>: {humidity} %\n<i>Давление:</i> {pressure} мм.рт.ст\n<i>Ветер:</i> {wind} м.с\n'
                     f'<i>Восход солнца:</i> {sunries_timestamp}\n<i>Закат солнца:</i> {sunset_timestamp}\n<i>Продолжительность дня:</i> {lenght_of_the_day}\n'
                     f'***<b>Хорошего вам дня</b>!***',
                     reply_markup=keyboard, parse_mode='HTML'
                     )   
        
    except Exception as err:
        bot.reply_to(message, f'Не удалось получить погоду для города {city}. Ошибка: {err}')

        


@bot.callback_query_handler(func=lambda call: call.data.startswith('forecast_2_days_'))
def forecast_3_days_handler(call):
    city = call.data.split('_')[-1]
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_token}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        forecast = {}
        for item in data['list'][:8]:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            day = dt.strftime('%Y-%m-%d')
            if day not in forecast:
                forecast[day] = {'temperature': []}
            forecast[day]['temperature'].append(item['main']['temp'])

        forecast_text = ''
        for day, values in forecast.items():
            temperature_max = round(max(values['temperature']))
            forecast_text += f"{day}: {temperature_max}°C\n"
        bot.send_message(
            call.message.chat.id, f'<b>Прогноз погоды на 2 дня:</b>\n{forecast_text}', parse_mode='HTML')
    else:
        bot.send_message(call.message.chat.id, f'Не удалось получить прогноз')


bot.polling(non_stop=True)
