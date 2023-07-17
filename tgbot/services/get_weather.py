import json
from datetime import datetime
from tgbot.services.api_request import request_to_api


def get_weather(coordinates, config):
    coordinates = coordinates.split()
    url = config.misc.weather_url
    querystring = {'lat': coordinates[1], 'lon': coordinates[0], 'lang': 'ru_RU'}
    headers = {'X-Yandex-API-Key': config.misc.weather_key}
    response = request_to_api(url=url, querystring=querystring, headers=headers)
    if response:
        try:
            result = json.loads(response.text)
        except Exception:
            result = None
        return result
    return None


def get_weather_result(weather_data):
    weather = dict()
    weather['location'] = weather_data.get('geo_object').get('locality').get('name')
    weather['now'] = {
        'date': datetime.now().strftime("%d.%m.%Y %H:%M"),
        'temperature': weather_data.get('fact').get('temp'),
        'condition': weather_data.get('fact').get('condition'),
        'wind_speed': weather_data.get('fact').get('wind_speed'),
        'pressure_mm': weather_data.get('fact').get('pressure_mm'),
    }
    weather['forecasts'] = []
    for date_item in weather_data.get('forecasts'):
        weather['forecasts'].append({
            'date': date_item.get('date'),
            'temperature_night': date_item.get('parts').get('night').get('temp_avg'),
            'condition_night': date_item.get('parts').get('night').get('condition'),
            'temperature_day': date_item.get('parts').get('day').get('temp_avg'),
            'condition_day': date_item.get('parts').get('day').get('condition'),
            'temperature_evening': date_item.get('parts').get('evening').get('temp_avg'),
            'condition_evening': date_item.get('parts').get('evening').get('condition'),
            'temperature_morning': date_item.get('parts').get('morning').get('temp_avg'),
            'condition_morning': date_item.get('parts').get('morning').get('condition'),
        })
    return weather
