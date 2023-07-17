CONDITIONS = {
    'clear': '☀️ясно',
    'partly-cloudy': '🌤 малооблачно',
    'cloudy': '🌤 облачно с прояснениями',
    'overcast': '☁️пасмурно',
    'drizzle': '🌧 морось',
    'light-rain': '🌧 небольшой дождь',
    'rain': '💧 дождь',
    'moderate-rain': '💦 умеренно сильный дождь',
    'heavy-rain': '💦 сильный дождь',
    'continuous-heavy-rain': '💦 длительный сильный дождь',
    'showers': '💦 ливень',
    'wet-snow': '❄️💧 дождь со снегом',
    'light-snow': '❄️небольшой снег',
    'snow': '❄️снег',
    'snow-showers': '❄️❄️❄️снегопад',
    'hail': '🧊 град',
    'thunderstorm': '⚡️гроза',
    'thunderstorm-with-rain': '💧⚡️дождь с грозой',
    'thunderstorm-with-hail': '🧊⚡️гроза с градом',
}


async def get_current_weather_str(weather_result: dict) -> str:
    return f"📆 <b>{weather_result.get('now').get('date')}, {weather_result.get('location')}:</b> \n" \
           f"<b>Температура</b>: {weather_result.get('now').get('temperature')}° " \
           f"({CONDITIONS[weather_result.get('now').get('condition')]})\n" \
           f"<b>Ветер</b>: {weather_result.get('now').get('wind_speed')} м/с\n" \
           f"<b>Атм. давление</b>: {weather_result.get('now').get('pressure_mm')} мм"


async def get_week_weather_list(weather_result: dict) -> list:
    result_list = []
    for data in weather_result.get('forecasts'):
        result_list.append(f"📆 <b>{data.get('date')}</b>\n"
                           f"<b>Ночь</b>: {data.get('temperature_night')}° "
                           f"({CONDITIONS[data.get('condition_night')]})\n"
                           f"<b>День</b>: {data.get('temperature_day')}° "
                           f"({CONDITIONS[data.get('condition_day')]})\n"
                           f"<b>Вечер</b>: {data.get('temperature_evening')}° "
                           f"({CONDITIONS[data.get('condition_evening')]})\n"
                           f"<b>Утро</b>: {data.get('temperature_morning')}° "
                           f"({CONDITIONS[data.get('condition_morning')]})")
    return result_list
