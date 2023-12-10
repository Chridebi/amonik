from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token

"""модуль содержит зависимость аутентификации, которая будет внедрена в наши маршруты для
принудительной аутентификации и авторизации."""
"""Обработка аутентификации пользователя"""


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)
    return decoded_token["user"]

"""В предыдущем блоке начинаем с импорта необходимых зависимостей:
• Depends: Это вводит oauth2_scheme в функцию в качестве зависимости.
• OAuth2PasswordBearer: Этот класс сообщает приложению, что схема
безопасности присутствует.
• verify_access_token: Эта функция, определенная в разделе создания и
проверки токена доступа, будет использоваться для проверки
действительности токена.Затем мы определяем URL токена для схемы OAuth2 и функцию аутентификации.
Функция аутентификации принимает токен в качестве аргумента. В функцию в
качестве зависимости внедрена схема OAuth. Токен декодируется, и
пользовательское поле полезной нагрузки возвращается, если токен
действителен, в противном случае возвращаются адекватные ответы об
ошибках, как определено в функции verify_access_token.

обновим поток аутентификации в маршрутах, а также добавим функцию
аутентификации в маршруты событий
"""