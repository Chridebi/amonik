"""обрабатывать операции маршрутизации,
такие как регистрация и вход пользователей"""
from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
"""маршрут регистрации"""
@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )
    await user_database.save(user)
    return {
        "message": "User created successfully"
    }
"""В этом блоке кода мы проверяем, существует ли такой пользователь с
переданным адресом электронной почты, прежде чем добавлять его в базу
данных."""

"""маршрут входа"""
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    if user_exist.password == user.password:
        return {
            "message": "User signed in successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )
"""мы сначала проверяем, существует ли
пользователь, прежде чем проверять действительность его учетных данных.
Используемый здесь метод аутентификации является базовым и не рекомендуется в
производственной среде."""
