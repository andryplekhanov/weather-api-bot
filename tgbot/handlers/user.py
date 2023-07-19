from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models import orm
from tgbot.services.set_bot_commands import get_default_commands


async def user_start(message: Message, state: FSMContext):
    await state.finish()
    # await orm.add_user(message.bot.get('db'), message.from_user.id)
    text = f'Привет, {message.from_user.username}! Я бот, который расскажет о погоде на сегодня.'
    await message.answer(text)
    commands = await get_default_commands()
    await message.answer(f"Я реагирую на следующие команды:\n\n{commands}")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
