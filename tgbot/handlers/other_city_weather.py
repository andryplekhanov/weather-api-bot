from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersInfo


async def other_city_weather(message: Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'other_city_weather'
    await message.answer('Введите город')
    await UsersInfo.city_geo.set()


def register_other_city_weather(dp: Dispatcher):
    dp.register_message_handler(other_city_weather, commands=['other_city_weather'], state='*')
