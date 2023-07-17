from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import Config
from tgbot.keyboards.inline import print_cities, show_forecast_callback, show_prev_next_callback
from tgbot.misc.states import UsersInfo
# from tgbot.models import orm
from tgbot.services.factories import for_city
from tgbot.services.get_cities import parse_cities_group
from tgbot.services.get_weather import get_weather, get_weather_result
from tgbot.services.ready_for_answer import get_current_weather_str, get_week_weather_list


async def get_cities_group(message: Message, config: Config, state: FSMContext):
    answer = message.text
    cities_list = parse_cities_group(city=answer, config=config)
    if cities_list:
        await message.answer("Пожалуйста, уточните:", reply_markup=print_cities(cities_list))
    else:
        await message.answer("⚠️ Не нахожу такой город. Введите ещё раз.")


async def clarify_city(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['city_geo'] = callback_data.get('city_geo')
        data['city_name'] = callback_data.get('city_name')

    # states = await state.get_data()
    # city_name = states.get('city_name')
    # city_geo = states.get('city_geo')
    # if states.get('last_command') == 'set_location':
    #     await orm.set_user_city(async_session=call.message.bot.get('db'),
    #                             city_name=city_name,
    #                             city_geo=city_geo,
    #                             user_id=call.message.chat.id)

    weather_data = get_weather(coordinates=callback_data.get('city_geo'), config=config)
    weather_result = get_weather_result(weather_data)
    reply_str = await get_current_weather_str(weather_result)
    await call.message.answer(reply_str, reply_markup=show_forecast_callback())
    await call.answer(cache_time=15)
    await state.finish()
    async with state.proxy() as data:
        data['result'] = weather_result
    await call.message.delete()


async def week_forecast(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=15)
    async with state.proxy() as data:
        weather_result = data.get('result')
        week_weather_datas = await get_week_weather_list(weather_result)
        data['result'] = week_weather_datas
    async with state.proxy() as data:
        current_page = 0
        data['current_page'] = current_page
        await call.message.answer(data.get('result')[current_page], reply_markup=show_prev_next_callback())


async def flipping_pages_back(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        current_page = data.get('current_page')
        if current_page == 0:
            current_page = 6
        else:
            current_page = current_page - 1
        data['current_page'] = current_page
    async with state.proxy() as data:
        await call.message.edit_text(
            data.get('result')[data.get('current_page')], reply_markup=show_prev_next_callback()
        )


async def flipping_pages_forward(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        current_page = data.get('current_page')
        if current_page == 6:
            current_page = 0
        else:
            current_page = current_page + 1
        data['current_page'] = current_page
    async with state.proxy() as data:
        await call.message.edit_text(
            data.get('result')[data.get('current_page')], reply_markup=show_prev_next_callback()
        )


def register_survey(dp: Dispatcher):
    dp.register_message_handler(get_cities_group, state=UsersInfo.city_geo)
    dp.register_callback_query_handler(clarify_city, for_city.filter(), state="*")
    dp.register_callback_query_handler(week_forecast, text='show_forecast', state="*")
    dp.register_callback_query_handler(flipping_pages_back, text='back', state="*")
    dp.register_callback_query_handler(flipping_pages_forward, text='forward', state="*")
