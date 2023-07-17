from typing import Tuple, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.services.factories import for_city


def print_cities(cities_list: List[Tuple]) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками - выбор подходящего по названию города, из которых пользователь выбирает нужный ему.
    :param cities_list: список кортежей с названиями городов и их геоданными.
    :return: клавиатура InlineKeyboardMarkup.
    """

    keyboard = InlineKeyboardMarkup()
    for data in cities_list:
        city_name = data[0][:19]
        keyboard.add(InlineKeyboardButton(text=f'{city_name} ({data[1]})',
                                          callback_data=for_city.new(city_geo=data[2], city_name=city_name)
                                          ))
    return keyboard


def show_forecast_callback() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - показать прогноз на 7 дней.
    :return: клавиатура InlineKeyboardMarkup.
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'Прогноз на 7 дней', callback_data='show_forecast'))
    return keyboard


def show_prev_next_callback() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками "Вперёд" и "Назад".
    :return: клавиатура InlineKeyboardMarkup.
    """

    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            InlineKeyboardButton(text=f'<<<', callback_data='back'),
            InlineKeyboardButton(text=f'>>>', callback_data='forward')
        ]
    ])
    return keyboard
