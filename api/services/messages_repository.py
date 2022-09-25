from api.models import models
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.mailing import MailingUpdate
from api.schemas.message import MessageCreate
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class MessagesRepository:
    def __init__(self, session):
        self.session: Session = session

    def get_all(self,
                ) -> list[models.Message]:

        query = (
            self.session
            .query(models.Message)
        )
        query = query.options(joinedload(models.Message.client))
        query = query.options(joinedload(models.Message.mailing))
        query = query.options(joinedload(models.Message.logs))
        execute = self.session.execute(query)

        db_message: list[models.Message] = execute.scalars().all()
        return db_message

    def get_by_client_mailing_ids(self,
                                  client_id: int,
                                  mailing_id: int,
                                  ) -> models.Message | None:
        query = (
            self.session
            .query(models.Message)
        )

        query = query.filter(models.Message.client_id == client_id, models.Message.mailing_id == mailing_id)
        query = query.options(joinedload(models.Message.client))
        query = query.options(joinedload(models.Message.mailing))
        query = query.options(joinedload(models.Message.logs))

        execute = self.session.execute(query)

        db_message: list[models.Message] = execute.scalar_one_or_none()
        return db_message

    def get_by_id(self,
                  model_id: int,
                  ) -> models.Message:

        query = (
            self.session
            .query(models.Message)
        )
        query = query.options(joinedload(models.Message.client))
        query = query.options(joinedload(models.Message.mailing))
        query = query.options(joinedload(models.Message.logs))
        query = query.filter(models.Message.id == model_id)
        execute = self.session.execute(query)

        db_model: models.Message | None = execute.scalar_one_or_none()
        return db_model

    def create(self,
               schemas_create: MessageCreate,
               ) -> models.Message:

        db_model = models.Message(**schemas_create.dict())
        self.session.add(db_model)
        self.session.flush()
        return db_model

    def update(self,
               db_model: models.Message,
               schema_update: MailingUpdate,
               ) -> models.Message:

        # model_update = models.Message(**schema_update.dict(exclude_unset=True))
        update_model(db_model, schema_update)
        self.session.flush()
        return db_model

    def delete(self,
               db_model: models.Message,
               ) -> None:

        if len(db_model.logs) != 0:
            db_model.logs.clear()

        self.session.delete(db_model)
        self.session.flush()
