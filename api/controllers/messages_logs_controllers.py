from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.logs.messages_logs_repository import \
    MessagesLogsRepository
from api.responses.json_response import (client_deleted_successfully,
                                         raise_client_not_found)
from api.responses.success import DELETED_SUCCESSFULLY


class MessagesLogsControllers:
    def __init__(self, session):
        self.session: AsyncSession = session
        self.messages_logs_repository = MessagesLogsRepository(session)

    def get_all(self):

        return self.messages_logs_repository.get_all()

    def get_all_by_mailing_id(self,
                              message_id: int):

        return self.messages_logs_repository.get_all_by_message_id(message_id=message_id)
