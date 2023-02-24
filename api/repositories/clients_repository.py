from sqlalchemy import delete, insert, update, values
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from api.models import models
from api.responses.json_response import raise_client_not_found, raise_db_exc
from api.responses.success import (DELETED_NOT_SUCCESSFULLY,
                                   DELETED_SUCCESSFULLY)
from api.schemas.client import ClientCreate, ClientUpdate
from api.utils.models_utils import update_model


class ClientsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[models.Client]:
        query = select(models.Client)
        query = query.options(selectinload(models.Client.messages))
        query = query.options(selectinload(models.Client.logs))
        execute = await self.session.execute(query)

        db_models: list[models.Client] = execute.scalars().all()
        return db_models

    async def get_all_by_filter(self, *,
                                phone_operator_code: str | None = None,
                                tag: str | None = None) -> list[models.Client]:
        query = select(models.Client)
        query = query.options(selectinload(models.Client.messages))
        query = query.options(selectinload(models.Client.logs))

        if phone_operator_code is not None:
            query.where(models.Client.phone_operator_code == phone_operator_code)

        if tag is not None:
            query.where(models.Client.tag == tag)

        execute = await self.session.execute(query)

        db_models: list[models.Client] = execute.scalars().all()
        return db_models

    async def get_by_id(self, *,
                        model_id: int) -> models.Client | None:
        query = select(models.Client)
        query = query.where(models.Client.id == model_id)
        query = query.options(selectinload(models.Client.messages))
        query = query.options(selectinload(models.Client.logs))
        execute = await self.session.execute(query)

        db_model: models.Client | None = execute.scalar_one_or_none()
        return db_model

    def create(self, model_create: ClientCreate) -> models.Client:

        db_model = models.Client.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, *,
               db_model: models.Client,
               model_update: ClientUpdate) -> models.Client:
        update_model(db_model,
                     model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, *,
                     db_model: models.Client) -> None:
        if len(db_model.messages) != 0:
            db_model.messages.clear()

        if len(db_model.logs) != 0:
            db_model.logs.clear()

        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, *,
                      db_model: models.Client):
        await self.session.refresh(db_model)
