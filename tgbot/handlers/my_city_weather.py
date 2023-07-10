from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersInfo


async def my_city_weather(message: Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'my_city_weather'

    await message.answer('Введите ваш город')
    await UsersInfo.city_geo.set()


def register_my_city_weather(dp: Dispatcher):
    dp.register_message_handler(my_city_weather, commands=['my_city_weather'], state='*')
