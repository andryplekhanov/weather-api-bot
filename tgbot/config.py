from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    name: str
    port: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    geocoder_key: str
    geocoder_url: str
    weather_key: str
    weather_url: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASSWORD'),
            user=env.str('DB_USER'),
            name=env.str('DB_NAME'),
            port=env.str('DB_PORT')
        ),
        misc=Miscellaneous(
            geocoder_key=env.str("GEOCODER"),
            geocoder_url=env.str("GEOCODER_URL"),
            weather_key=env.str("YANDEX_WEATHER"),
            weather_url=env.str("YANDEX_WEATHER_URL"),
        )
    )
