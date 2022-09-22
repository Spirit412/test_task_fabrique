import json
from enum import Enum, IntEnum
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.logs.client_log import ClientLogCreate
from api.schemas.logs.log_base import LoggerLevelsEnum, LoggerActionsEnum
from api.schemas.logs.mailing_log import MailingLogCreate
from api.schemas.logs.message_log import MessageLogCreate
from api.services.logs.client_logs_repository import ClientLogsRepository
from api.services.logs.mailings_logs_repository import MailingsLogsRepository
from api.services.logs.messages_logs_repository import MessagesLogsRepository


class Logger:
    """
    Утилита для логирование различных событий в базу данных
    """

    def __init__(self, session):
        self.session: AsyncSession = session

        self._client_logs_repository = ClientLogsRepository(session)
        self._mailings_logs_repository = MailingsLogsRepository(session)
        self._messages_logs_repository = MessagesLogsRepository(session)

    async def create_client_log(self, client_id: int | None, level: LoggerLevelsEnum, action: LoggerActionsEnum,
                                message_text: str, data: dict = {}):
        """
        Создаёт лог связанный с изменениями клиента
        """

        log_create = ClientLogCreate(
            client_id=client_id, level=int(level), action=int(action),
            message_text=message_text, data_json=json.dumps(data)
        )

        self._client_logs_repository.create(log_create)
        await self._client_logs_repository.commit()

    async def create_mailing_log(self, mailing_id: int | None, level: LoggerLevelsEnum, action: LoggerActionsEnum,
                                 message_text: str, data: dict = {}):
        """
        Создаёт лог связанный с изменениями клиента
        """

        log_create = MailingLogCreate(
            mailing_id=mailing_id, level=int(level), action=int(action),
            message_text=message_text, data_json=json.dumps(data)
        )

        self._mailings_logs_repository.create(log_create)
        await self._mailings_logs_repository.commit()

    async def create_message_log(self, message_id: int | None, level: LoggerLevelsEnum, action: LoggerActionsEnum,
                                 message_text: str, data: dict = {}):
        """
        Создаёт лог связанный с изменениями клиента
        """

        log_create = MessageLogCreate(
            message_id=message_id, level=int(level), action=int(action),
            message_text=message_text, data_json=json.dumps(data)
        )

        self._messages_logs_repository.create(log_create)
        await self._messages_logs_repository.commit()
