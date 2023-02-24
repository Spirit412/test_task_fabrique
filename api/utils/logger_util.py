import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.logs.client_logs_repository import ClientLogsRepository
from api.repositories.logs.mailings_logs_repository import \
    MailingsLogsRepository
from api.repositories.logs.messages_logs_repository import \
    MessagesLogsRepository
from api.schemas.logs.client_log import ClientLogCreate
from api.schemas.logs.log_base import LoggerActionsEnum, LoggerLevelsEnum
from api.schemas.logs.mailing_log import MailingLogCreate
from api.schemas.logs.message_log import MessageLogCreate


class Logger:
    """
    Утилита для логирование различных событий в базу данных
    """

    def __init__(self, session):
        self.session: AsyncSession = session

        self._client_logs_repository = ClientLogsRepository(session)
        self._mailings_logs_repository = MailingsLogsRepository(session)
        self._messages_logs_repository = MessagesLogsRepository(session)

    def create_client_log(self,
                          client_id: int | None,
                          level: LoggerLevelsEnum,
                          action: LoggerActionsEnum,
                          message_text: str,
                          data: dict = {},
                          ):
        """
        Создаёт лог связанный с изменениями клиента
        """

        log_create = ClientLogCreate(client_id=client_id,
                                     level=int(level),
                                     action=int(action),
                                     message_text=message_text,
                                     data_json=jsonable_encoder(data),
                                     )

        self._client_logs_repository.create(model_create=log_create,
                                            )
        return True

    def create_mailing_log(self,
                           mailing_id: int | None,
                           level: LoggerLevelsEnum,
                           action: LoggerActionsEnum,
                           message_text: str,
                           data: dict = {},
                           ):
        """
        Создаёт лог связанный с изменениями клиента
        """

        log_create = MailingLogCreate(mailing_id=mailing_id,
                                      level=int(level),
                                      action=int(action),
                                      message_text=message_text,
                                      data_json=json.dumps(data),
                                      )

        self._mailings_logs_repository.create(model_create=log_create,
                                              )

    def create_message_log(self,
                           message_id: int | None,
                           level: LoggerLevelsEnum,
                           action: LoggerActionsEnum,
                           message_text: str,
                           data: dict = {},
                           ):
        """
        Создаёт лог связанный с изменениями клиента
        """

        log_create = MessageLogCreate(message_id=message_id,
                                      level=int(level),
                                      action=int(action),
                                      message_text=message_text,
                                      data_json=json.dumps(data),
                                      )

        self._messages_logs_repository.create(model_create=log_create,
                                              )
