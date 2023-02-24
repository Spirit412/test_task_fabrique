from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.logs.mailing_log import (MailingLog, MailingLogCreate,
                                          MailingLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload, selectinload
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, insert, update, values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class MailingsLogsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[models.MailingLog]:
        query = select(models.MailingLog)
        query = query.options(selectinload(models.MailingLog.mailing))
        execute = await self.session.execute(query)

        db_models: list[models.MailingLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> models.MailingLog | None:
        query = select(models.MailingLog)
        query = query.where(models.MailingLog.id == model_id)
        query = query.options(selectinload(models.MailingLog.mailing))
        execute = await self.session.execute(query)

        db_model: Optional[models.MailingLog] = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_mailing_id(self, mailing_id: int) -> list[models.MailingLog]:
        query = select(models.MailingLog)
        query = query.where(models.MailingLog.mailing_id == mailing_id)
        query = query.options(selectinload(models.MailingLog.mailing))
        execute = await self.session.execute(query)

        db_models: list[models.MailingLog] = execute.scalars().all()
        return db_models

    def create(self, model_create: MailingLogCreate) -> models.MailingLog:
        db_model = MailingLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: models.MailingLog, model_update: MailingLogUpdate) -> models.MailingLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: models.MailingLog) -> None:
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: models.MailingLog):
        await self.session.refresh(db_model)
