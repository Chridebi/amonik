import asyncio
import httpx
import pytest
from main import app
from database.connection import Settings
from models.events import Event
from models.users import User

"""В предыдущем блоке кода мы импортировали модули asyncio, httpx и
pytest. Модуль asyncio будет использоваться для создания активного сеанса
цикла, чтобы тесты выполнялись в одном потоке, чтобы избежать конфликтов.
Тест httpx будет действовать как асинхронный клиент для выполнения
CRUD операций HTTP. Библиотека pytest необходима для определения
фикстур.
Мы также импортировали приложение-экземпляр нашего приложения, а также модели
и класс Settings. Давайте определим фикстуру сеанса цикла: """

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()

"""Сейчас мы используем новую базу данных testdb.

определим клиентскую фикстуру по умолчанию, которая
возвращает экземпляр нашего приложения, работающего асинхронно через
httpx:
"""

@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client

        # Clean up resources
        await Event.find_all().delete()
        await User.find_all().delete()

"""сначала инициализируется база данных, а приложение
запускается как AsyncClient, который остается активным до конца тестового
сеанса. В конце сеанса тестирования коллекция событий и пользователей
стирается, чтобы убедиться, что база данных пуста перед каждым запуском
теста."""

# await User.find_all().delete()

