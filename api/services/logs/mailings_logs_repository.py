from api.models import models
from api.schemas.logs.mailing_log import (MailingLog, MailingLogCreate,
                                          MailingLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MailingsLogsRepository:

    def get_all(self, *,
                session: Session,
                ) -> list[models.MailingLog]:

        query = (
            session
            .query(models.MailingLog)
            .options(joinedload(models.MailingLog.mailing))
        )
        execute = session.execute(query)

        db_models: list[models.MailingLog] = execute.scalars().all()
        return db_models

    def get_by_id(self, *,
                  session: Session,
                  model_id: int,
                  ) -> models.MailingLog | None:
        query = (
            session
            .query(models.MailingLog)
            .options(joinedload(models.MailingLog.mailing))
        )
        query = query.filter(models.MailingLog.id == model_id)
        execute = session.execute(query)

        db_model: models.MailingLog | None = execute.scalar_one_or_none()
        return db_model

    def get_all_by_mailing_id(self, *,
                              session: Session,
                              mailing_id: int,
                              ) -> list[models.MailingLog]:

        query = (
            session
            .query(models.MailingLog)
            .options(joinedload(models.MailingLog.mailing))
        )
        query = query.filter(models.MailingLog.mailing_id == mailing_id)
        execute = session.execute(query)
        db_models: list[models.MailingLog] = execute.scalars().all()
        return db_models

    def create(self, *,
               session: Session,
               model_create: MailingLogCreate,
               ) -> models.MailingLog:

        db_model = MailingLog.from_orm(model_create)
        db_model = models.MailingLog(**model_create.dict())
        session.add(db_model)
        session.flush()
        return db_model

    def update(self, *,
               session: Session,
               db_model: MailingLog,
               model_update: MailingLogUpdate,
               ) -> models.MailingLog:

        model_update = models.MailingLog(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        session.flush()

    def delete(self, *,
               session: Session,
               db_model: models.MailingLog,
               ) -> None:

        session.delete(db_model)
        session.flush()
