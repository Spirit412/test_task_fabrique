from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.logs.client_logs_repository import ClientLogsRepository
from api.responses.json_response import (client_deleted_successfully,
                                         raise_client_not_found)
from api.responses.success import DELETED_SUCCESSFULLY


class ClientLogsControllers:
    def __init__(self, session):
        self.session: AsyncSession = session
        self.client_logs_repository = ClientLogsRepository(session)

    def get_all(self):

        return self.client_logs_repository.get_all()

    def get_all_by_client_id(self,
                             client_id: int):

        return self.client_logs_repository.get_all_by_client_id(client_id=client_id)
