from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.logs.client_log import (ClientLog, ClientLogCreate,
                                         ClientLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload
from fastapi.encoders import jsonable_encoder


class ClientLogsRepository:
    def __init__(self, session):
        self.session: Session = session

    def get_all(self,
                ) -> list[models.ClientLog]:
        query = (
            self.session
            .query(models.ClientLog)
            .options(joinedload(models.ClientLog.client))
        )
        execute = self.session.execute(query)

        db_models: list[models.ClientLog] = execute.scalars().all()
        return db_models

    def get_by_id(self,
                  model_id: int,
                  ) -> models.ClientLog | None:
        query = (
            self.session
            .query(models.ClientLog)
            .options(joinedload(models.ClientLog.client))
        )

        query = query.filter(models.ClientLog.id == model_id)
        execute = self.session.execute(query)

        db_model: models.ClientLog | None = execute.scalar_one_or_none()
        return db_model

    def get_all_by_client_id(self,
                             client_id: int,
                             ) -> list[models.ClientLog]:
        query = (
            self.session
            .query(models.ClientLog)
            .options(joinedload(models.ClientLog.client))
        )

        query = query.filter(models.ClientLog.client_id == client_id)
        execute = self.session.execute(query)

        db_models: list[models.ClientLog] = execute.scalars().all()
        return db_models

    def create(self,
               model_create: ClientLogCreate,
               ) -> models.ClientLog:

        db_model = models.ClientLog(**model_create.dict())
        self.session.add(db_model)
        self.session.flush()
        return db_model

    def update(self,
               db_model: models.ClientLog,
               model_update: ClientLogUpdate,
               ) -> models.ClientLog:

        # model_update = models.ClientLog(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        self.session.flush()
        return db_model

    def delete(self,
               db_model: models.ClientLog,
               ) -> None:

        self.session.delete(db_model)
        self.session.flush()
