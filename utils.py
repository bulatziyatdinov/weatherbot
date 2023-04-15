import requests
import os
from dotenv import load_dotenv


# Загрузка из файла конфига config.json
def get_settings_form_file() -> dict:
    try:
        load_dotenv()
        data = {
            'BOT_TOKEN': os.getenv('BOT_TOKEN'),
            'DB_NAME': os.getenv('DB_NAME'),
            'OPENWEATHER_TOKEN': os.getenv('OPENWEATHER_TOKEN'),
            'ADMIN': [int(os.getenv('ADMIN'))],
        }
        return data
    except Exception as ex:
        print('Ошибка на стадии инициализации конфига', ex)


# Город по геолокации
def get_city_lat_lon(lat, lon, token):
    params = {
        "appid": str(token),
        "lang": "ru",
        "units": "metric",
        "mode": "JSON",
        "lat": str(lat),
        "lon": str(lon),
    }
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather",
                            params=params).json()
    return response['name']


# Получение погоды
def get_weather_city(city, token):
    params = {
        "q": city,
        "appid": str(token),
        "lang": "ru",
        "units": "metric",
        "mode": "JSON",
    }

    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather",
                                params=params).json()
        status = int(response['cod'])
        if status == 404 or city.strip().lower() == 'none':
            return 'Город не найден\nПопробуйте поменять свой город через команду /set_city *ваш город*'
        elif status == 200:
            weather = response['weather'][0]['description'].capitalize()

            main = response['main']

            wind = response['wind']['speed']

            clouds = response['clouds']['all']

            answer = f"Город: {response['name']}\n" \
                     '----------------------\n' \
                     f"Погода: {weather}\n" \
                     f"Температура: {main['temp']}°\n" \
                     f"Ощущается как: {main['feels_like']}°\n" \
                     f"Давление: {round(main['pressure'] * 0.750064, 1)} мм рт. ст.\n" \
                     f"Влажность: {main['humidity']}%\n" \
                     f"Скорость ветра: {wind} м/с\n" \
                     f"Облачность: {clouds}%"
            return answer
        else:
            return 'Неизвестная ошибка'
    except Exception as ex:
        print('Ошибка в API', ex)
        return 'Ошибка в API запроса погоды\nПопробуйте воспользоваться сервисом позже'
