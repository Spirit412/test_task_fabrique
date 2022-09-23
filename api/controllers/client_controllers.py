from sqlalchemy.orm import Session
from api.models import models
from api.responses.exceptions import raise_client_not_found
from api.schemas.client import ClientCreate
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum
from api.services.clients_repository import ClientsRepository


class ClientControllers:
    def __init__(self, session):
        self.session: Session = session
        self._clients_repository = ClientsRepository(session)
        self._logger = Logger(session)

    def get_all(self,
                ):

        db_clients = self._clients_repository.get_all()

        return db_clients

    def get_by_id(self,
                  get_by_id: int,
                  ):
        db_client: models.Client | None = self._clients_repository.get_by_id(model_id=get_by_id)
        if db_client:
            return db_client
        raise_client_not_found(get_by_id)

    def create(self,
               model_create: ClientCreate,
               ):

        db_client: models.Client | None = self._clients_repository.create(model_create=model_create)

        self._logger.create_client_log(client_id=db_client.id,
                                       level=LoggerLevelsEnum.DEBUG,
                                       action=LoggerActionsEnum.CREATE,
                                       message_text=f"Client ID:{db_client.id} Created",
                                       )
        return db_client

    def update(self,
               ):
        pass

    def delete(self,
               ):
        pass
