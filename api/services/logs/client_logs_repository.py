from api.models import models
from api.schemas.logs.client_log import (ClientLog, ClientLogCreate,
                                         ClientLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class ClientLogsRepository:

    def get_all(self, *,
                session: Session,
                ) -> list[models.ClientLog]:
        query = (
            session
            .query(models.ClientLog)
            .options(joinedload(models.ClientLog.client))
        )
        execute = session.execute(query)

        db_models: list[models.ClientLog] = execute.scalars().all()
        return db_models

    def get_by_id(self, *,
                  session: Session,
                  model_id: int,
                  ) -> models.ClientLog | None:
        query = (
            session
            .query(models.ClientLog)
            .options(joinedload(models.ClientLog.client))
        )

        query = query.filter(models.ClientLog.id == model_id)
        execute = session.execute(query)

        db_model: models.ClientLog | None = execute.scalar_one_or_none()
        return db_model

    def get_all_by_client_id(self, *,
                             session: Session,
                             client_id: int,
                             ) -> list[models.ClientLog]:
        query = (
            session
            .query(models.ClientLog)
            .options(joinedload(models.ClientLog.client))
        )

        query = query.filter(models.ClientLog.client_id == client_id)
        execute = session.execute(query)

        db_models: list[models.ClientLog] = execute.scalars().all()
        return db_models

    def create(self, *,
               session: Session,
               model_create: ClientLogCreate,
               ) -> models.ClientLog:
        db_model = ClientLog.from_orm(model_create)

        db_model = models.ClientLog(**model_create.dict())
        session.add(db_model)
        session.flush()
        return db_model

    def update(self, *,
               session: Session,
               db_model: models.ClientLog,
               model_update: ClientLogUpdate,
               ) -> models.ClientLog:

        model_update = models.ClientLog(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        session.flush()

    def delete(self, *,
               session: Session,
               db_model: models.ClientLog,
               ) -> None:

        session.delete(db_model)
        session.flush()
