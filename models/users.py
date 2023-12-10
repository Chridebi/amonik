"""определение модели для пользовательских операций."""
from pydantic import BaseModel, EmailStr

from beanie import Document


class User(Document):
    email: EmailStr
    password: str

    class Collection:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
