import logging

from sqlalchemy import select

from tgbot.models.models import User

logger = logging.getLogger(__name__)


async def add_user(async_session, user_id):
    async with async_session() as session:
        user = await session.execute(select(User).where(User.tg_id == user_id))
        all_users = user.scalars().all()
        # logger.info(f"Users: {all_users}")

        if str(user_id) not in list(map(str, all_users)):
            new_user = User(tg_id=user_id)
            session.add(new_user)
            await session.commit()
            logger.info(f"User '{user_id}' was added to DB")


async def set_user_city(async_session, user_id, city_name, city_geo):
    async with async_session() as session:
        responce = await session.execute(select(User).where(User.tg_id == user_id))
        all_users = responce.scalars().all()
        user = all_users[0]
        user.city_name = city_name
        user.city_geo = city_geo
        await session.commit()
        logger.info(f"City added for User '{user.tg_id}' == {user.city_name}")


async def get_users_city(async_session, user_id):
    async with async_session() as session:
        try:
            responce = await session.execute(select(User).where(User.tg_id == user_id))
            all_users = responce.scalars().all()
            user = all_users[0]
            return user.city_geo
        except Exception:
            return None
