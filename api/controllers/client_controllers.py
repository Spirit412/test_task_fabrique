from sqlalchemy.orm import Session
from api.models import models
from api.responses.json_response import client_deleted_successfully, raise_client_not_found
from api.responses.success import DELETED_SUCCESSFULLY
from api.schemas.client import ClientCreate, ClientUpdate
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum
from api.services.clients_repository import ClientsRepository


class ClientControllers:
    def __init__(self, session):
        self.session: Session = session
        self.clients_repository = ClientsRepository(session)
        self.logger = Logger(session)

    def get_all(self,
                ):

        db_clients = self.clients_repository.get_all()
        return db_clients

    def get_by_id(self,
                  get_by_id: int,
                  ):
        db_client: models.Client | None = self.clients_repository.get_by_id(model_id=get_by_id)
        if db_client:
            return db_client
        else:
            raise_client_not_found(client_id=get_by_id)

    def create(self,
               model_create: ClientCreate,
               ):

        db_client: models.Client | None = self.clients_repository.create(model_create)

        self.logger.create_client_log(client_id=db_client.id,
                                      level=LoggerLevelsEnum.DEBUG,
                                      action=LoggerActionsEnum.CREATE,
                                      message_text=f"Client ID:{db_client.id} Created",
                                      )
        return db_client

    def update(self,
               client_id: int,
               client_update: ClientUpdate,
               ):

        db_client: models.Client | None = self.clients_repository.get_by_id(model_id=client_id)
        if db_client:
            db_client = self.clients_repository.update(db_model=db_client,
                                                       model_update=client_update,
                                                       )
            self.session.commit()
            self.logger.create_client_log(client_id=db_client.id,
                                          level=LoggerLevelsEnum.DEBUG,
                                          action=LoggerActionsEnum.UPDATE,
                                          message_text=f"ID:{client_id} Client Updated",
                                          )

            return db_client

        else:
            self.logger.create_client_log(client_id=None,
                                          level=LoggerLevelsEnum.ERROR,
                                          action=LoggerActionsEnum.UPDATE,
                                          message_text=f"ID:{client_id} Client Not Found")

            raise_client_not_found(client_id=client_id)

    def delete(self,
               client_id: int,
               ):

        db_client: models.Client | None = self.clients_repository.get_by_id(model_id=client_id)

        if db_client:
            self.clients_repository.delete(db_client)
            self.logger.create_client_log(client_id=db_client.id,
                                          level=LoggerLevelsEnum.DEBUG,
                                          action=LoggerActionsEnum.DELETE,
                                          message_text=f"ID:{client_id} Client Deleted",
                                          )
            client_deleted_successfully(client_id=client_id)

        else:
            self.logger.create_client_log(client_id=None,
                                          level=LoggerLevelsEnum.ERROR,
                                          action=LoggerActionsEnum.DELETE,
                                          message_text=f"ID:{client_id} Client Not Found")

            raise_client_not_found(client_id=client_id)
