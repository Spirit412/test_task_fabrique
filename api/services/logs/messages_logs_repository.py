from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.logs.message_log import (MessageLog, MessageLogCreate,
                                          MessageLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MessagesLogsRepository:
    def __init__(self, session):
        self.session: Session = session

    def get_all(self,
                ) -> list[models.MessageLog]:
        query = (
            self.session
            .query(models.MessageLog)
            .options(joinedload(models.MessageLog.message))
        )

        execute = self.session.execute(query)

        db_models: list[models.MessageLog] = execute.scalars().all()
        return db_models

    def get_by_id(self,
                  model_id: int,
                  ) -> models.MessageLog | None:
        query = (
            self.session
            .query(models.MessageLog)
            .options(joinedload(models.MessageLog.message))
        )
        query = query.filter(models.MessageLog.id == model_id)
        execute = self.session.execute(query)

        db_model: models.MessageLog | None = execute.scalar_one_or_none()
        return db_model

    def get_all_by_message_id(self,
                              message_id: int,
                              ) -> list[models.MessageLog]:
        query = (
            self.session
            .query(models.MessageLog)
            .options(joinedload(models.MessageLog.message))
        )
        query = query.filter(models.MessageLog.message_id == message_id)
        execute = self.session.execute(query)

        db_models: list[models.MessageLog] = execute.scalars().all()
        return db_models

    def create(self,
               model_create: MessageLogCreate,
               ) -> models.MessageLog:

        db_model = MessageLog.from_orm(model_create)
        db_model = models.MessageLog(**model_create.dict())
        self.session.add(db_model)
        self.session.flush()
        return db_model

    def update(self,
               db_model: MessageLog,
               model_update: MessageLogUpdate,
               ) -> models.MessageLog:

        # model_update = models.MessageLog(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        self.session.flush()

    def delete(self,
               db_model: MessageLog,
               ) -> None:

        self.session.delete(db_model)
        self.session.flush()
