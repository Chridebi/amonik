"""модуль содержит функции, необходимые для кодирования и
декодирования строк JWT"""

import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from database.database import Settings

settings = Settings()


def create_access_token(user: str):
    payload = {
        "user": user,
        "expires": time.time() + 3600
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


"""функция принимает строковый аргумент, который
передается в словарь полезной нагрузки. Словарь полезной нагрузки содержит
пользователя и время истечения срока действия, которое возвращается при
декодировании JWT
Срок действия устанавливается равным часу с момента создания. Затем полезная
нагрузка передается методу encode(), который принимает три параметра:
• Payload: Словарь, содержащий значения для кодирования.
• Key: Ключ, используемый для подписи полезной нагрузки.
• Algorithm: Алгоритм, используемый для подписи полезной нагрузки.
По умолчанию и наиболее распространенным является алгоритм HS256.
"""

"""функцию для проверки подлинности токена, отправленного в
наше приложение:"""


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )
        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )


"""функция принимает в качестве аргумента строку токена и
выполняет несколько проверок в блоке try. Сначала функция проверяет срок
действия токена. Если срок действия не указан, значит, токен не был предоставлен.
Вторая проверка — валидность токена — генерируется исключение, информирующее
пользователя об истечении срока действия токена. Если токен действителен,
возвращается декодированная полезная нагрузка.
В блоке except для любой ошибки JWT выдается исключение неверного запроса"""
