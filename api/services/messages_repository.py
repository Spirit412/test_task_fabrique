from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY
from api.schemas.mailing import MailingUpdate
from api.schemas.message import MessageCreate
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MessagesRepository:

    def get_all(self, *,
                session: Session,
                ) -> list[models.Message]:

        query = (
            session
            .query(models.Message)
        )
        query = query.options(joinedload(models.Message.client))
        query = query.options(joinedload(models.Message.mailing))
        query = query.options(joinedload(models.Message.logs))
        execute = session.execute(query)

        db_message: list[models.Message] = execute.scalars().all()
        return db_message

    def get_by_client_mailing_ids(self, *,
                                  session: Session,
                                  client_id: int,
                                  mailing_id: int,
                                  ) -> models.Message | None:
        query = (
            session
            .query(models.Message)
        )

        query = query.filter(models.Message.client_id == client_id, models.Message.mailing_id == mailing_id)
        query = query.options(joinedload(models.Message.client))
        query = query.options(joinedload(models.Message.mailing))
        query = query.options(joinedload(models.Message.logs))

        execute = session.execute(query)

        db_message: list[models.Message] = execute.scalar_one_or_none()
        return db_message

    def get_by_id(self, *,
                  session: Session,
                  model_id: int,
                  ) -> models.Message:

        query = (
            session
            .query(models.Message)
        )
        query = query.options(joinedload(models.Message.client))
        query = query.options(joinedload(models.Message.mailing))
        query = query.options(joinedload(models.Message.logs))
        query = query.filter(models.Message.id == model_id)
        execute = session.execute(query)

        db_model: models.Message | None = execute.scalar_one_or_none()
        return db_model

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
               schema_update: MailingUpdate,
               ) -> models.Message:

        model_update = models.Message(**schema_update.dict(exclude_unset=True))
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
        session.flush()
