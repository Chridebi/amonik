from typing import Optional

from beanie import init_beanie
from models.events import Event
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from sqlmodel import SQLModel, create_engine


database_file = "database.db"
engine = create_engine(database_file, echo=True)
SQLModel.metadata.create_all(engine)

class Settings(BaseSettings):
    SECRET_KEY: Optional[str] = None

    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[Event, User])

    class Config:
        env_file = ".env"
