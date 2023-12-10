from passlib.context import CryptContext
"""модуль содержит функции, которые будут использоваться для шифрования пароля пользователя при регистрации и
сравнения паролей при входе."""

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


class HashPassword:
    """
        Метод create_hash принимает строку и возвращает хешированное значение.
        метод verify_hash берет простой пароль и хешированный пароль и сравнивает
    их. Функция возвращает логическое значение, указывающее, совпадают ли
    переданные значения или нет."""

    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    """обновим маршрут регистрации, чтобы хешировать пароль пользователя перед
его сохранением в базе данных"""
    """CryptContext, который использует схему bcrypt для 
хеширования переданных ему строк"""
