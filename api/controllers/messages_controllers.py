from sqlalchemy.ext.asyncio import AsyncSession

from api.models import models
from api.repositories.messages_repository import MessagesRepository
from api.responses.json_response import (message_deleted_successfully,
                                         raise_message_not_found)
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum


class MessagesControllers:
    def __init__(self, session):
        self.session: AsyncSession = session
        self.messages_repository = MessagesRepository(session)
        self.logger = Logger(session)

    def get_all(self,
                ):

        db_clients = self.messages_repository.get_all()
        return db_clients

    def get_by_id(self,
                  message_id: int,
                  ):

        db_message: models.Message | None = self.messages_repository.get_by_id(model_id=message_id)
        if db_message:
            return db_message
        else:
            raise_message_not_found(message_id)

    def delete(self,
               message_id: int,
               ):

        db_message: models.Message | None = self.messages_repository.get_by_id(model_id=message_id)
        if db_message:
            self.messages_repository.delete(db_model=db_message)
            self.logger.create_message_log(None,
                                           LoggerLevelsEnum.DEBUG,
                                           LoggerActionsEnum.DELETE,
                                           f"ID:{message_id} Message Deleted")
            message_deleted_successfully(message_id)

        else:
            self.logger.create_message_log(None,
                                           LoggerLevelsEnum.ERROR,
                                           LoggerActionsEnum.DELETE,
                                           f"ID:{message_id} Message Not Found")
            raise_message_not_found(message_id=message_id)
