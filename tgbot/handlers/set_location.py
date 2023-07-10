from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersInfo


async def set_location(message: Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'set_location'
    await message.answer('Введите ваш город')
    await UsersInfo.city_geo.set()


def register_set_location(dp: Dispatcher):
    dp.register_message_handler(set_location, commands=['set_location'], state='*')
