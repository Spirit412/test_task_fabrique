from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.logs.mailing_log import (MailingLog, MailingLogCreate,
                                          MailingLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MailingsLogsRepository:
    def __init__(self, session):
        self.session: Session = session

    def get_all(self,
                ) -> list[models.MailingLog]:

        query = (
            self.session
            .query(models.MailingLog)
            .options(joinedload(models.MailingLog.mailing))
        )
        execute = self.session.execute(query)

        db_models: list[models.MailingLog] = execute.scalars().all()
        return db_models

    def get_by_id(self,
                  model_id: int,
                  ) -> models.MailingLog | None:
        query = (
            self.session
            .query(models.MailingLog)
            .options(joinedload(models.MailingLog.mailing))
        )
        query = query.filter(models.MailingLog.id == model_id)
        execute = self.session.execute(query)

        db_model: models.MailingLog | None = execute.scalar_one_or_none()
        return db_model

    def get_all_by_mailing_id(self,
                              mailing_id: int,
                              ) -> list[models.MailingLog]:

        query = (
            self.session
            .query(models.MailingLog)
            .options(joinedload(models.MailingLog.mailing))
        )
        query = query.filter(models.MailingLog.mailing_id == mailing_id)
        execute = self.session.execute(query)
        db_models: list[models.MailingLog] = execute.scalars().all()
        return db_models

    def create(self,
               model_create: MailingLogCreate,
               ) -> models.MailingLog:

        db_model = MailingLog.from_orm(model_create)
        db_model = models.MailingLog(**model_create.dict())
        self.session.add(db_model)
        self.session.flush()
        return db_model

    def update(self,
               db_model: MailingLog,
               model_update: MailingLogUpdate,
               ) -> models.MailingLog:

        # model_update = models.MailingLog(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        self.session.flush()

    def delete(self, *,
               session: Session,
               db_model: models.MailingLog,
               ) -> None:

        session.delete(db_model)
        session.flush()
