from aiogram.dispatcher.filters.state import StatesGroup, State


class UsersInfo(StatesGroup):
    city_geo = State()
    city_name = State()
    result = State()
    current_page = State()
    last_command = State()
