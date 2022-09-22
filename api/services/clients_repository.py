from api import schemas
from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class ClientsRepository:

    def get_one(self, *,
                session: Session,
                client_id: int,
                ) -> models.Client:

        query = (
            session
            .query(models.Client)
        )
        query = query.options(joinedload('messages'))
        query = query.options(joinedload('logs'))
        query = query.filter(
            models.Client.id == client_id)
        return query.one_or_none()

    def index(self, *,
              session: Session,
              phone_operator_code: str | None = None,
              tag: str | None = None,
              offset: int = 0,
              limit: int = 20,
              ) -> list[models.Client]:

        query = (
            session
            .query(models.Client)
        )
        query = query.options(joinedload('messages'))
        query = query.options(joinedload('logs'))

        query = query.filter(models.Client.tag == tag) if tag is not None else query
        query = query.filter(models.Client.phone_operator_code == phone_operator_code) if phone_operator_code is not None else query

        return query.offset(offset).limit(limit).all()

    def create(self, *,
               session: Session,
               schemas_create: schemas.ClientCreate,
               ) -> models.Message:
        db_model = models.Client(**schemas_create.dict())

        self.session.add(db_model)
        session.flush()
        return db_model

    def update(self, *,
               session: Session,
               db_model: models.Client,
               cshema_update: schemas.ClientUpdate,
               ) -> models.Client:

        model_update = models.Client(**cshema_update.dict(exclude_unset=True))
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
