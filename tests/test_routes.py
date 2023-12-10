"""Тестирование конечных точек CRUD """

import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

"""создадим новую фикстуру, которая при
вызове возвращает токен доступа. Приспособление имеет область модуля, что
означает, что оно запускается только один раз — при выполнении тестового
модуля — и не вызывается при каждом вызове функции. """


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@packt.com")

"""создадим новый прибор, который добавляет событие в базу данных. Это
действие выполняется для запуска предварительных тестов перед тестированием
конечных точек CRUD"""


@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="We will be discussing the contents of\
        the FastAPI book in this event.Ensure to come with\
        your own copy to win gifts!",
        tags=["python", "fastapi", "book", "launch"],
        location="Google Meet"
        )
    await Event.insert_one(new_event)
    yield new_event

"""тестовую функцию, которая проверяет GET-метод HTTP на
маршруте /event"""


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

    """мы тестируем путь маршрута события, чтобы проверить,
присутствует ли событие, добавленное в базу данных в фикстуре mock_event"""

"""тестовую функцию для конечной точки /event/{id}"""


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)

    """мы тестируем конечную точку, которая извлекает одно
событие. Переданный идентификатор события извлекается из фикстуры mock_event,
а результат запроса сравнивается с данными, хранящимися в фикстуре mock_event """

"""тестовую функцию для создания нового события 
Тестирование конечной точки CREATE
начнем с определения функции и получения токена доступа из ранее
созданного прибора. Мы создадим полезную нагрузку запроса, которая будет
отправлена на сервер, заголовки запроса, которые будут содержать тип контента, а
также значение заголовка авторизации. Также будет определен тестовый ответ,
после чего инициируется запрос и сравниваются ответы."""


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "We will be discussing the contents\
        of the FastAPI book in this event.Ensure to come\
        with your own copy to win gifts!",
        "tags": [
            "python",
            "fastapi",
            "book",
            "launch"
        ],
        "location": "Google Meet",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {
        "message": "Event created successfully"
    }

    response = await default_client.post("/event/new",
                        json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response

"""тест для проверки количества событий, хранящихся в базе данных
(в нашем случае 2)."""


@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.
    AsyncClient) -> None:
        response = await default_client.get("/event/")

        events = response.json()

        assert response.status_code == 200
        assert len(events) == 2

""" мы сохранили ответ JSON в переменной events, длина
которой используется для нашего тестового сравнения"""

"""Тестирование конечной точки UPDATE"""


@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient,
    mock_event: Event, access_token: str) -> None:
    test_payload = {
        "title": "Updated FastAPI event"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{str(mock_event.id)}"
    response = await default_client.put(url,
                        json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]

    test_payload["title"]

"""мы изменяем событие, хранящееся в базе данных,
извлекая ID из фикстуры mock_event Затем мы определяем полезную нагрузку
запроса и заголовки. В переменной response инициируется запрос и сравнивается
полученный ответ."""

"""Тестирование конечной точки DELETE"""


@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient,
    mock_event: Event, access_token: str) -> None:
    test_response = {
        "message": "Event deleted successfully."
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"/event/{mock_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response

"""определяется ожидаемый ответ теста, а также заголовки.
Маршрут DELETE задействован, и ответ сравнивается"""

"""Чтобы убедиться, что документ действительно был удален, добавим финальную
проверку"""


@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)

"""когда вы успешно реализовали тесты для аутентификации и
маршрутов событий, раскомментируйте код, отвечающий за очистку
пользовательских данных из базы данных await User.find_all().delete()"""

"""Покрытие тестами 

открыть htmlcov/index.html в своем браузере"""
