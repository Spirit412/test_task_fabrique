import logging
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.sqlalchemy_async_connection import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.logger = logging.getLogger(__name__)

    async def get(self, session: AsyncSession, *, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(
            self.model.id == id
        )
        coro = await session.execute(stmt)
        db_obj = coro.scalar()
        return db_obj

    async def get_index(self, session: AsyncSession) -> List[ModelType]:
        stmt = select(self.model)
        coro = await session.execute(stmt)
        db_obj_list = coro.scalars()
        return db_obj_list

    async def create(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, session: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = db_obj.__dict__
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        return db_obj

    async def delete(self, session: AsyncSession, *, id: int) -> Optional[int]:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        c = await session.execute(stmt)
        rm_id, = c.one()
        await session.commit()
        return rm_id
