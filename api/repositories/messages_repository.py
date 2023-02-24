from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models import models
from api.responses.success import (DELETED_NOT_SUCCESSFULLY,
                                   DELETED_SUCCESSFULLY)
from api.schemas.mailing import MailingUpdate
from api.schemas.message import MessageCreate, MessageUpdate
from api.utils.models_utils import update_model


class MessagesRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[models.Message]:
        query = select(models.Message)
        query = query.options(selectinload(models.Message.client))
        query = query.options(selectinload(models.Message.mailing))
        query = query.options(selectinload(models.Message.logs))
        execute = await self.session.execute(query)

        db_models: list[models.Message] = execute.scalars().all()
        return db_models

    async def get_by_client_mailing_ids(self, client_id: int, mailing_id: int) -> models.Message | None:
        query = select(models.Message)
        query = query.where(models.Message.client_id == client_id, models.Message.mailing_id == mailing_id)
        query = query.options(selectinload(models.Message.client))
        query = query.options(
            selectinload(models.Message.mailing))
        query = query.options(selectinload(models.Message.logs))
        execute = await self.session.execute(query)

        db_message: list[models.Message] = execute.scalar_one_or_none()
        return db_message

    async def get_by_id(self, model_id: int) -> models.Message | None:
        query = select(models.Message)
        query = query.where(models.Message.id == model_id)
        query = query.options(selectinload(models.Message.client))
        query = query.options(selectinload(models.Message.mailing))
        query = query.options(selectinload(models.Message.logs))
        execute = await self.session.execute(query)

        db_model: models.Message | None = execute.scalar_one_or_none()
        return db_model

    def create(self, model_create: MessageCreate) -> models.Message:
        db_model = models.Message.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: models.Message, model_update: MessageUpdate) -> models.Message:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: models.Message) -> None:
        if len(db_model.logs) != 0:
            db_model.logs.clear()

        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: models.Message):
        await self.session.refresh(db_model)
