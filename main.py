import telebot
import requests
from currency_converter import CurrencyConverter



WEATHER_API_KEY = 'e3f6b05f3f457188c53ebdc0d225b875'


c = CurrencyConverter()

bot = telebot.TeleBot('6506416216:AAHnJm-0tOggeHLnn7zIn4x4tJBsMKYZDHQ')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для отображения погоды и курса валют. Используйте /weather и /currency.")

@bot.message_handler(commands=['weather'])
def get_weather(message):
    # Используем ReplyKeyboardMarkup для отправки сообщения с кнопкой для ввода города
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    msg = bot.reply_to(message, "Введите город:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)

def process_city_step(message):
    try:
        city = message.text
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(weather_api_url)
        data = response.json()

        if data["cod"] == "404":
            bot.reply_to(message, "Город не найден.")
        else:
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            bot.reply_to(message, f"Температура: {temperature}°C\nПогода: {weather_description}")

    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так. Пожалуйста, повторите попытку.")

@bot.message_handler(commands=['currency'])
def get_currency(message):
    # Используем ReplyKeyboardMarkup для отправки сообщения с кнопками для ввода валют
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('USD', 'EUR', 'GBP', 'JPY')
    msg = bot.reply_to(message, "Выберите базовую валюту:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_currency_step)

def process_currency_step(message):
    try:
        base_currency = message.text
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row('USD', 'EUR', 'GBP', 'JPY')
        msg = bot.reply_to(message, "Выберите целевую валюту:", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: process_target_currency_step(m, base_currency))

    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так. Пожалуйста, повторите попытку.")

def process_target_currency_step(message, base_currency):
    try:
        target_currency = message.text
        rate = c.convert(1, base_currency, target_currency)
        bot.reply_to(message, f"Курс: 1 {base_currency} = {rate} {target_currency}")

    except Exception as e:
        bot.reply_to(message, "Что-то пошло не так. Пожалуйста, повторите попытку.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
