from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY
from api.schemas.mailing import MailingUpdate
from api.schemas.message import MessageCreate
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MessageRepository:

    def get_one(self, *,
                session: Session,
                message_id: int,
                ) -> models.Message:

        query = (
            session
            .query(models.Message)
        )
        query = query.options(joinedload('client'))
        query = query.options(joinedload('mailing'))
        query = query.options(joinedload('logs'))
        query = query.filter(
            models.Message.id == message_id)
        return query.one_or_none()

    def index(self, *,
              session: Session,
              client_id: int | None = None,
              mailing_id: int | None = None,

              tag: str | None = None,
              offset: int = 0,
              limit: int = 20,
              ) -> list[models.Message]:

        query = (
            session
            .query(models.Message)
        )
        query = query.options(joinedload('client'))
        query = query.options(joinedload('mailing'))
        query = query.options(joinedload('logs'))

        query = query.filter(models.Message.client_id == client_id) if client_id is not None else query
        query = query.filter(models.Message.mailing_id == mailing_id) if mailing_id is not None else query

        return query.offset(offset).limit(limit).all()

    def create(self, *,
               session: Session,
               schemas_create: MessageCreate,
               ) -> models.Message:
        db_model = models.Message(**schemas_create.dict())

        self.session.add(db_model)
        session.flush()
        return db_model

    def update(self, *,
               session: Session,
               db_model: models.Message,
               cshema_update: MailingUpdate,
               ) -> models.Message:

        model_update = models.Message(**cshema_update.dict(exclude_unset=True))
        update_model(db_model, model_update)
        session.flush()

        return db_model

    def delete(self, *,
               session: Session,
               db_model: models.Message,
               ) -> None:

        if len(db_model.logs) != 0:
            db_model.logs.clear()

        session.delete(db_model)
        return DELETED_SUCCESSFULLY
