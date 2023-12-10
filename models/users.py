"""определение модели для пользовательских операций."""
from pydantic import BaseModel, EmailStr

from beanie import Document


class User(Document):
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
