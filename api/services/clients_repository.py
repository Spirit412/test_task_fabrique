from api import schemas
from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY
from api.schemas.client import ClientCreate, ClientUpdate
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class ClientsRepository:

    def get_all(self, *,
                session: Session,
                phone_operator_code: str | None = None,
                tag: str | None = None,
                ) -> list[models.Client]:

        query = (
            session
            .query(models.Client)
        )
        query = query.options(joinedload(models.Client.messages))
        query = query.options(joinedload(models.Client.logs))
        execute = session.execute(query)

        db_models: list[models.Client] = execute.scalars().all()
        return db_models

    def get_all_by_filter(self, *,
                          session: Session,
                          phone_operator_code: str | None = None,
                          tag: str | None = None,
                          ) -> list[models.Client]:

        query = (
            session
            .query(models.Client)
        )
        query = query.options(joinedload(models.Client.messages))
        query = query.options(joinedload(models.Client.logs))

        query = query.filter(models.Client.phone_operator_code == phone_operator_code) if phone_operator_code is not None else query
        query = query.filter(models.Client.tag == tag) if tag is not None else query
        execute = session.execute(query)

        db_models: list[models.Client] = execute.scalars().all()
        return db_models

    def get_by_id(self, *,
                  session: Session,
                  model_id: int,
                  ) -> models.Client:

        query = (
            session
            .query(models.Client)
        )
        query = query.options(joinedload(models.Client.messages))
        query = query.options(joinedload(models.Client.logs))

        query = query.filter(models.Client.id == model_id)
        execute = session.execute(query)

        db_model: models.Client | None = execute.scalar_one_or_none()
        return db_model

    def create(self, *,
               session: Session,
               model_create: ClientCreate,
               ) -> models.Message:
        
        db_model = models.Client(**model_create.dict())
        session.add(db_model)
        session.flush()
        return db_model

    def update(self, *,
               session: Session,
               db_model: models.Client,
               model_update: ClientUpdate,
               ) -> models.Client:

        model_update = models.Client(**model_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        session.flush()
        return db_model

    async def delete(self, *,
                     session: Session,
                     db_model: models.Client,
                     ) -> None:

        if len(db_model.messages) != 0:
            db_model.messages.clear()

        if len(db_model.logs) != 0:
            db_model.logs.clear()

        session.delete(db_model)
        session.flush()
