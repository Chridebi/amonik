from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from models.events import Event
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, BaseModel

from sqlmodel import SQLModel, Session, create_engine

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}
engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)


def conn():
    SQLModel.metadata.create_all(engine_url)


def get_session():
    with Session(engine_url) as session:
        yield session


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[Event, User])

    class Config:
        env_file = ".env"


"""класс Database, который принимает модель в качестве аргумента во время инициализации:
Модель, передаваемая во время инициализации, представляет собой класс
модели документа Event или User"""

"""Создать: метод save для получения документа, который будет экземпляром документа, 
    переданного в экземпляр Database в момент создания экземпляра."""

"""Читать: метод, get(), принимает идентификатор в качестве аргумента метода и
    возвращает соответствующую запись из базы данных, в то время как метод get_all()
    не принимает аргументов и возвращает список всех записей, имеющихся в базе данных"""

"""Обновить: метод для обработки процесса обновления существующей записи"""
"""В этом блоке кода метод update принимает ID и ответственную схему Pydantic,
которая будет содержать поля, обновленные из запроса PUT отправленного
клиентом. Обновленное тело запроса сначала анализируется в словаре, а затем
фильтруется для удаления значений None.
Как только это будет сделано, он вставляется в запрос на обновление, который,
наконец, выполняется методом update() Beanie."""

"""Удалить: метод для удаления записи из базы данных"""
"""код метод проверяет, существует ли такая запись, прежде чем
приступить к ее удалению из базы данных.
Далее обновим маршруты"""


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
