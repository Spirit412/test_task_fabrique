from api.schemas.logs.mailing_log import (MailingLog, MailingLogCreate,
                                          MailingLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MailingsLogsRepository:

    async def get_all(self, *,
                      session: Session,
                      ) -> list[MailingLog]:
        query = select(MailingLog).options(selectinload(MailingLog.mailing))
        execute = await self.session.execute(query)

        db_models: list[MailingLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, *,
                        session: Session,
                        model_id: int,
                        ) -> MailingLog | None:
        query = select(MailingLog).where(MailingLog.id == model_id).options(selectinload(MailingLog.mailing))
        execute = await self.session.execute(query)

        db_model: MailingLog | None = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_mailing_id(self, *,
                                    session: Session,
                                    mailing_id: int,
                                    ) -> list[MailingLog]:
        query = select(MailingLog).where(MailingLog.mailing_id == mailing_id).options(selectinload(MailingLog.mailing))
        execute = await self.session.execute(query)

        db_models: list[MailingLog] = execute.scalars().all()
        return db_models

    def create(self, *,
               session: Session,
               model_create: MailingLogCreate,
               ) -> MailingLog:
        db_model = MailingLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, *,
               session: Session,
               db_model: MailingLog,
               model_update: MailingLogUpdate,
               ) -> MailingLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, *,
                     session: Session,
                     db_model: MailingLog,
                     ) -> None:
        await self.session.delete(db_model)
