from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('my_city_weather', "Погода в моём городе"),
    ('other_city_weather', "Погода в другом городе"),
    ('set_location', "Установить свой город"),
    ('history', "История поиска")
)


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[BotCommand(*i) for i in DEFAULT_COMMANDS],
        scope=BotCommandScopeDefault()
    )


async def get_default_commands():
    return '\n'.join([f'<b>/{command}</b> - {desc}' for command, desc in DEFAULT_COMMANDS])
