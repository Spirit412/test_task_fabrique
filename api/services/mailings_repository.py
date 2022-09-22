from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.mailing import Mailing, MailingCreate, MailingUpdate
from api.utils.models_utils import update_model
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload


class MailingsRepository:
    def __init__(self, session):
        self.session: Session = session

    def get_all(self,
                ) -> list[models.Mailing]:
        query = (
            self.session
            .query(models.Mailing)
        )
        query = query.options(joinedload(models.Mailing.messages))
        query = query.options(joinedload(models.Mailing.logs))
        execute = self.session.execute(query)

        db_models: list[models.Mailing] = execute.scalars().all()
        return db_models

    def get_by_id(self,
                  model_id: int,
                  ) -> models.Mailing:

        query = (
            self.session
            .query(models.Mailing)
        )
        query = query.options(joinedload(models.Mailing.messages))
        query = query.options(joinedload(models.Mailing.logs))
        query = query.filter(models.Mailing.id == model_id)
        execute = self.session.execute(query)

        db_model: models.Mailing | None = execute.scalar_one_or_none()
        return db_model

    def get_by_date_activation(self,
                               current_date,
                               ) -> list[Mailing]:
        query = (
            self.session
            .query(models.Mailing)
        )
        query = query.filter(models.Mailing.sending_start_date <= current_date, current_date <= models.Mailing.sending_end_date)
        query = query.options(joinedload(models.Mailing.messages))
        query = query.options(joinedload(models.Mailing.logs))
        execute = self.session.execute(query)

        db_models: list[models.Mailing] = execute.scalars().all()
        return db_models

    def create(self,
               model_create: MailingCreate,
               ) -> models.Mailing:

        db_model = models.Mailing(**model_create.dict())
        self.session.add(db_model)
        self.session.flush()
        return db_model

    def update(self,
               db_model: Mailing,
               model_update: MailingUpdate,
               ) -> models.Mailing:

        model_update = models.Mailing(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        self.session.add(db_model)
        self.session.flush()
        return db_model

    def delete(self,
               db_model: Mailing,
               ) -> None:
        if len(db_model.logs) != 0:
            db_model.logs.clear()

        if len(db_model.messages) != 0:
            db_model.messages.clear()
        self.session.delete(db_model)
        self.session.flush()
