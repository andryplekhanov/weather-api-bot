import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.help import register_help
from tgbot.handlers.my_city_weather import register_my_city_weather
from tgbot.handlers.other_city_weather import register_other_city_weather
from tgbot.handlers.set_location import register_set_location
from tgbot.handlers.survey import register_survey
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.models.models import Base
from tgbot.models.utils import make_connection_string
from tgbot.services.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_help(dp)
    register_set_location(dp)
    register_other_city_weather(dp)
    register_my_city_weather(dp)
    register_survey(dp)

    register_echo(dp)


async def set_all_commands(bot: Bot):
    await set_default_commands(bot)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # Creating DB engine for PostgreSQL
    engine = create_async_engine(make_connection_string(config=config), future=True, echo=False)

    # Creating DB connections pool
    db_pool = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    bot["db"] = db_pool

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    await set_default_commands(bot)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
