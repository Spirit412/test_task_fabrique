from api.models import models
from api.responses.json_response import raise_client_not_found, raise_db_exc
from api.responses.success import DELETED_SUCCESSFULLY, DELETED_NOT_SUCCESSFULLY
from api.schemas.client import ClientCreate, ClientUpdate
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exc
from psycopg2 import errors
import re


class ClientsRepository:
    def __init__(self, session):
        self.session: Session = session

    def get_all(self,
                ) -> list[models.Client]:

        query = (
            self.session
            .query(models.Client)
        )
        query = query.options(joinedload(models.Client.messages))
        query = query.options(joinedload(models.Client.logs))
        execute = self.session.execute(query)

        db_models: list[models.Client] = execute.scalars().all()
        return db_models

    def get_all_by_filter(self,
                          phone_operator_code: str | None = None,
                          tag: str | None = None,
                          ) -> list[models.Client]:

        query = (
            self.session
            .query(models.Client)
        )
        query = query.options(joinedload(models.Client.messages))
        query = query.options(joinedload(models.Client.logs))

        query = query.filter(models.Client.phone_operator_code == phone_operator_code) if phone_operator_code is not None else query
        query = query.filter(models.Client.tag == tag) if tag is not None else query
        execute = self.session.execute(query)

        db_models: list[models.Client] = execute.scalars().all()
        return db_models

    def get_by_id(self,
                  model_id: int,
                  ) -> models.Client:

        query = (
            self.session
            .query(models.Client)
            .filter(models.Client.id == model_id)
            .options(joinedload(models.Client.messages))
            .options(joinedload(models.Client.logs))
        )
        execute = self.session.execute(query)
        return execute.scalar_one_or_none()

    def create(self,
               model_create: ClientCreate,
               ) -> models.Message:

        db_model = models.Client(**model_create.dict())
        try:
            self.session.add(db_model)
            self.session.flush()
        except errors.UniqueViolation as e2:
            print("= " * 20)
            print(e2.DETAIL)
            print("= " * 20)
            self.session.rollback()
            return None
        except exc.IntegrityError as e1:
            raise_db_exc(re.sub("DETAIL:  ", "", str(e1).split('\n')[1]))
        return db_model

    def update(self,
               db_model: models.Client,
               model_update: ClientUpdate,
               ) -> models.Client:

        # model_update = models.Client(**model_update.dict(exclude_unset=True))
        update_model(db_model=db_model, model_update=model_update)
        try:
            self.session.flush()
        except exc.IntegrityError as e1:
            print("= " * 20)
            print(e1)
            print("= " * 20)
            self.session.rollback()
        except errors.UniqueViolation as e2:
            print("= " * 20)
            print(e2)
            print("= " * 20)
            self.session.rollback()
        return db_model

    def delete(self,
               db_model: models.Client,
               ) -> None:

        if len(db_model.messages) != 0:
            db_model.messages.clear()

        if len(db_model.logs) != 0:
            db_model.logs.clear()

        self.session.delete(db_model)
        self.session.flush()
