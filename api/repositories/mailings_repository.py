from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.mailing import MailingCreate, MailingUpdate
from api.utils.models_utils import update_model
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class MailingsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[models.Mailing]:
        query = select(models.Mailing)
        query = query.options(selectinload(models.Mailing.messages))
        query = query.options(selectinload(models.Mailing.logs))
        execute = await self.session.execute(query)

        db_models: list[models.Mailing] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> models.Mailing | None:
        query = select(models.Mailing)
        query = query.where(models.Mailing.id == model_id)
        query = query.options(selectinload(models.Mailing.messages))
        query = query.options(selectinload(models.Mailing.logs))
        execute = await self.session.execute(query)

        db_model: models.Mailing | None = execute.scalar_one_or_none()
        return db_model

    async def get_by_date_activation(self, current_date) -> list[models.Mailing]:
        query = select(models.Mailing).where(
            models.Mailing.sending_start_date <= current_date, current_date <= models.Mailing.sending_end_date)
        query = query.options(selectinload(models.Mailing.messages))
        query = query.options(selectinload(models.Mailing.logs))
        execute = await self.session.execute(query)

        db_models: list[models.Mailing] = execute.scalars().all()
        return db_models

    def create(self, model_create: MailingCreate) -> models.Mailing:
        db_model = models.Mailing.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: models.Mailing, model_update: MailingUpdate) -> models.Mailing:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: models.Mailing) -> None:
        if len(db_model.logs) != 0:
            db_model.logs.clear()

        if len(db_model.messages) != 0:
            db_model.messages.clear()
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: models.Mailing):
        await self.session.refresh(db_model)
