from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ContentType

from markups import keyboard_geo, keyboard_weather

from database import Database
import utils

# Чтение файла конфига
CONFIG = utils.get_settings_form_file()

# Создание бота
bot = Bot(CONFIG['BOT_TOKEN'], parse_mode='HTML')
dp = Dispatcher(bot)

# Подключение к БД
db = Database(CONFIG['DB_NAME'])

# Подключение к API
OPENWEATHER_TOKEN = CONFIG['OPENWEATHER_TOKEN']

# Список админов
ADMINS = CONFIG['ADMIN']


@dp.message_handler(commands=['start', 'старт'])
async def start(message: types.Message):
    db.add_user_to_db(message.chat.id)
    answer = 'Здравствуйте!\n' \
             'Установите город: /set_city *город*\n'
    await bot.send_message(message.chat.id, answer)
    answer = 'Команды:\n' \
             '----------------------\n' \
             'Список команд: /help\n' \
             'Узнать погоду: /weather\n' \
             'Установить город: /set_city *город*\n' \
             'Установить город по геопозиции: /set_city_geo\n' \
             'Информация использования: /info\n' \
             'Узнать город: /city *город*\n' \
             'Узнать кол-во использований: /nums\n'
    await bot.send_message(message.chat.id, answer, reply_markup=keyboard_geo)


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    city = utils.get_city_lat_lon(lat, lon, OPENWEATHER_TOKEN)
    db.set_user_city(message.chat.id, city)
    await message.answer('Город установлен!', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    answer = 'Команды:\n' \
             '------------\n' \
             'Список команд: /help:\n' \
             'Узнать погоду: /weather\n' \
             'Установить город: /set_city *город*\n' \
             'Установить город по геопозиции: /set_city_geo\n' \
             'Информация использования: /info\n' \
             'Узнать город: /city *город*\n' \
             'Узнать кол-во использований: /nums\n'
    await bot.send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['add_num'])
async def add_num(message: types.Message):
    try:
        if message.chat.id in ADMINS:
            db.update_nums_of_using(message.chat.id)
    except Exception as ex:
        print('Ошибка в главном файле!', ex)
        await bot.send_message(message.chat.id, 'Ошибка!')


@dp.message_handler(commands=['set_city'])
async def set_city(message: types.Message):
    city = ' '.join(message.text.strip().split()[1:])
    answer = db.set_user_city(message.chat.id, city)
    if answer:
        await bot.send_message(message.chat.id, 'Город успешно выбран!',
                               reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Ошибка в выборе города!',
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['set_city_geo'])
async def set_city_geo(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте нам геопозицию',
                           reply_markup=keyboard_geo)


@dp.message_handler(commands=['city'])
async def city(message: types.Message):
    try:
        answer = db.get_user_city(message.chat.id)
        answer = 'Ваш город:\n> ' + answer
        await bot.send_message(message.chat.id, answer)
    except Exception as ex:
        print('Ошибка в главном файле!', ex)
        await bot.send_message(message.chat.id, 'Ошибка!',
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['nums'])
async def nums(message: types.Message):
    try:
        answer = str(db.get_user_nums(message.chat.id))
        answer = 'Вы использовали бота:\n> ' + answer
        await bot.send_message(message.chat.id, answer)
    except Exception as ex:
        print('Ошибка в главном файле!', ex)
        await bot.send_message(message.chat.id, 'Ошибка!',
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    try:
        city = db.get_user_city(message.chat.id)
        nums = str(db.get_user_nums(message.chat.id))
        answer = 'Ваш город:\n> ' + city + '\n'
        answer += 'Вы использовали бота:\n> ' + nums
        await bot.send_message(message.chat.id, answer)
    except Exception as ex:
        print('Ошибка в главном файле!', ex)
        await bot.send_message(message.chat.id, 'Ошибка!',
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    city = db.get_user_city(message.chat.id)
    answer, picture = utils.get_weather_city(city, OPENWEATHER_TOKEN)
    db.update_nums_of_using(message.chat.id)
    await bot.send_photo(message.chat.id, photo=picture, caption=answer,
                         reply_markup=keyboard_weather)


@dp.callback_query_handler(text='weather_request')
async def vote_for_seva_def(message: types.CallbackQuery):
    city = db.get_user_city(message.from_user.id)
    answer, picture = utils.get_weather_city(city, OPENWEATHER_TOKEN)
    db.update_nums_of_using(message.from_user.id)
    await bot.send_photo(message.from_user.id, photo=picture, caption=answer,
                         reply_markup=keyboard_weather)


@dp.message_handler(content_types=ContentType.PHOTO)
async def photo(message: types.Message):
    await message.reply(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
