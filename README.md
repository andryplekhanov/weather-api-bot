# Weather Telegram-bot

Telegram-бот, написанный на AIOgram, показывающий погоду в выбранном городе.
Работает через API Яндекса.

- **Language** (язык): Russian
- **Author** (Автор): [Андрей Плеханов](https://t.me/andryplekhanov)

## Используемые технологии:
- Python 3
- AIOgram
- PostgreSQL (пользователи и их города сохраняются в БД)
- ORM SQLAlchemy
- Docker / Docker-compose

## Как запустить бота (должен быть запущен Docker):
- Клонировать репозиторий
- Создать telegram-бота у [BotFather](https://t.me/BotFather) и получить токен
- Получить ключи для API от Геокодера и Яндекс-погоды (инструкция [здесь](https://stepik.org/course/124179/) в главе 1.3)
- Файл **.env.dist** переименовать в **.env** и прописать там BOT_TOKEN, GEOCODER и YANDEX_WEATHER
- Запустить бота в Docker-контейнере: `docker-compose up —-build` (первый запуск может занять продолжительное время)
- Остановить бота командой: `Crtl+C`

## Возможности бота:

**Бот реагирует на команды:**

- **/start** — Запустить бота
- **/help** — Вывести справку
- **/my_city_weather** — Погода в моём городе
- **/other_city_weather** — Погода в другом городе
- **/set_location** — Установить свой город

