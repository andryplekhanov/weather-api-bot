from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import Config
from tgbot.keyboards.inline import show_forecast_callback
from tgbot.misc.states import UsersInfo
from tgbot.models.orm import get_users_city
from tgbot.services.get_weather import get_weather, get_weather_result
from tgbot.services.ready_for_answer import get_current_weather_str


async def my_city_weather(message: Message, state: FSMContext, config: Config):
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'my_city_weather'

    users_city = await get_users_city(async_session=message.bot.get('db'), user_id=message.from_user.id)
    if users_city:
        weather_data = await get_weather(coordinates=users_city, config=config)
        weather_result = await get_weather_result(weather_data)
        async with state.proxy() as data:
            data['result'] = weather_result
        reply_str = await get_current_weather_str(weather_result)
        await message.answer(reply_str, reply_markup=show_forecast_callback())
        await message.delete()
    else:
        await message.answer("Введите ваш город")
        await UsersInfo.city_geo.set()


def register_my_city_weather(dp: Dispatcher):
    dp.register_message_handler(my_city_weather, commands=['my_city_weather'], state='*')
