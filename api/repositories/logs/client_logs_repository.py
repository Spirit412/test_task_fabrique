from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, insert, update, values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models import models
from api.responses.success import (DELETED_NOT_SUCCESSFULLY,
                                   DELETED_SUCCESSFULLY)
from api.schemas.logs.client_log import (ClientLog, ClientLogCreate,
                                         ClientLogUpdate)
from api.utils.models_utils import update_model


class ClientLogsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[models.ClientLog]:
        select(models.ClientLog)
        query = query.options(selectinload(models.ClientLog.client))
        execute = await self.session.execute(query)

        db_models: list[models.ClientLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> models.ClientLog | None:
        query = select(models.ClientLog)
        query = query.where(models.ClientLog.id == model_id)
        query = query.options(selectinload(models.ClientLog.client))
        execute = await self.session.execute(query)

        db_model: ClientLog | None = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_client_id(self, client_id: int) -> list[models.ClientLog]:
        query = select(models.ClientLog)
        query = query.where(models.ClientLog.client_id == client_id)
        query = query.options(selectinload(models.ClientLog.client))
        execute = await self.session.execute(query)

        db_models: list[models.ClientLog] = execute.scalars().all()
        return db_models

    def create(self, model_create: ClientLogCreate) -> models.ClientLog:
        db_model = ClientLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: models.ClientLog, model_update: ClientLogUpdate) -> models.ClientLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: models.ClientLog) -> None:
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: models.ClientLog):
        await self.session.refresh(db_model)
