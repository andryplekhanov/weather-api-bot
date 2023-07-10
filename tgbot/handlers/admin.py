from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def admin_start(message: Message, state: FSMContext):
    await state.finish()
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
