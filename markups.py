from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Создание клавиатур
keyboard_geo = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_weather = InlineKeyboardMarkup()

# Создание кнопок
button_geo = KeyboardButton(text="Отправить своё местоположение\nТолько для телефонов", request_location=True)
button_weather = InlineKeyboardButton(text="Узнать погоду", callback_data='weather_request')

# Добавление кнопок в клавиатуры
keyboard_geo.add(button_geo)
keyboard_weather.add(button_weather)
