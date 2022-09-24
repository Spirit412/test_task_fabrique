from api.models import models
from api.responses.json_response import (client_deleted_successfully,
                                         mailing_deleted_successfully,
                                         raise_client_not_found,
                                         raise_mailing_not_found)
from api.responses.success import DELETED_SUCCESSFULLY
from api.schemas.client import ClientCreate, ClientDB, ClientUpdate
from api.schemas.mailing import MailingCreate, MailingUpdate
from api.services.mailings_repository import MailingsRepository
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum
from sqlalchemy.orm import Session


class MailingsControllers:
    def __init__(self, session):
        self.session: Session = session
        self.mailings_repository = MailingsRepository(session)
        self.logger = Logger(session)

    def get_all(self,
                ):

        db_clients = self.mailings_repository.get_all()
        return db_clients

    def get_by_id(self,
                  mailing_id: int,
                  ):

        db_mailing: models.Mailing | None = self.mailings_repository.get_by_id(model_id=mailing_id)
        if db_mailing:
            return mailing_id
        raise_mailing_not_found(mailing_id)

    def create(self,
               mailing_create: MailingCreate,
               ):

        db_mailing = self.mailings_repository.create(model_create=mailing_create)

        self.logger.create_mailing_log(db_mailing.id,
                                       LoggerLevelsEnum.DEBUG,
                                       LoggerActionsEnum.CREATE,
                                       f"ID:{db_mailing.id} Mailing Created")

        return db_mailing

    def update(self,
               mailing_id: int,
               mailing_update: MailingUpdate,
               ):

        db_mailing: models.Mailing | None = self.mailings_repository.get_by_id(model_id=mailing_id)
        if db_mailing:
            db_mailing = self.mailings_repository.update(db_mailing, mailing_update)
            self.logger.create_mailing_log(db_mailing.id,
                                           LoggerLevelsEnum.DEBUG,
                                           LoggerActionsEnum.UPDATE,
                                           f"ID:{mailing_id} Mailing Updated")
            return db_mailing

        self.logger.create_mailing_log(None,
                                       LoggerLevelsEnum.ERROR,
                                       LoggerActionsEnum.DELETE,
                                       f"ID:{mailing_id} Mailing Not Found")
        raise_mailing_not_found(mailing_id)

    def delete(self,
               mailing_id: int,
               ):

        db_mailing: models.Mailing | None = self.mailings_repository.get_by_id(mailing_id)
        if db_mailing:
            self.mailings_repository.delete(db_model=db_mailing)
            self.logger.create_mailing_log(None,
                                           LoggerLevelsEnum.DEBUG,
                                           LoggerActionsEnum.DELETE,
                                           f"ID:{mailing_id} Mailing Deleted")
            return mailing_deleted_successfully(mailing_id)

        self.logger.create_mailing_log(None,
                                       LoggerLevelsEnum.ERROR,
                                       LoggerActionsEnum.DELETE,
                                       f"ID:{mailing_id} Mailing Not Found")
        raise_mailing_not_found(mailing_id)
