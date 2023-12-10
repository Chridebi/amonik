import httpx
import pytest

"""Тестирование маршрута регистрации.
Первая конечная точка, которую мы будем тестировать, — это конечная точка
регистрации. Мы добавим декоратор pytest.mark.asyncio, который сообщает
pytest что нужно рассматривать это как асинхронный тест. Давайте определим
функцию и полезную нагрузку запроса:"""

@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
    "email": "testuser@packt.com",
    "password": "testpassword",
    }

"""Определим заголовок запроса и ожидаемый ответ"""
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
    }
    test_response = {
    "message": "User created successfully"
    }

    response = await default_client.post("/user/signup", json=payload, headers=headers)

    """проверим, был ли запрос успешным, сравнив ответы"""
    assert response.status_code == 200
    assert response.json() == test_response

"""Тестирование маршрута входа"""
@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "testpassword"
    }
    """payload = {
        "username": "wronguser@packt.com",
        "password": "testpassword"
    }"""

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

"""инициируем запрос и тестируем ответы"""
    response = await default_client.post("/user/signin",
                        data=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"

"""изменим имя пользователя для входа на неправильное, чтобы подтвердить,
что тест не пройден:"""

"""Мы успешно написали тесты для маршрутов регистрации и входа. Перейдем к
тестированию CRUD-маршрутов для API планировщика событий"""
