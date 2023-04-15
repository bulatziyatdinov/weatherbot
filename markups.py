from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_1 = KeyboardButton(text="Отправить своё местоположение\nТолько для телефонов", request_location=True)

keyboard.add(button_1)