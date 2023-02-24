from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, insert, update, values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload, selectinload

from api.models import models
from api.responses.success import (DELETED_NOT_SUCCESSFULLY,
                                   DELETED_SUCCESSFULLY)
from api.schemas.logs.message_log import (MessageLog, MessageLogCreate,
                                          MessageLogUpdate)
from api.utils.models_utils import update_model


class MessagesLogsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[models.MessageLog]:
        query = select(models.MessageLog)
        query = query.options(selectinload(models.MessageLog.message))
        execute = await self.session.execute(query)

        db_models: list[models.MessageLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> models.MessageLog | None:
        query = select(models.MessageLog)
        query = query.where(models.MessageLog.id == model_id)
        query = query.options(selectinload(models.MessageLog.message))
        execute = await self.session.execute(query)

        db_model: models.MessageLog | None = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_message_id(self, message_id: int) -> list[models.MessageLog]:
        query = select(models.MessageLog)
        query = query.where(models.MessageLog.message_id == message_id)
        query = query.options(selectinload(models.MessageLog.message))
        execute = await self.session.execute(query)

        db_models: list[models.MessageLog] = execute.scalars().all()
        return db_models

    def create(self, model_create: MessageLogCreate) -> models.MessageLog:
        db_model = MessageLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: models.MessageLog, model_update: MessageLogUpdate) -> models.MessageLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: models.MessageLog) -> None:
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: models.MessageLog):
        await self.session.refresh(db_model)
