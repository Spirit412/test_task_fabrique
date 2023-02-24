from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.logs.mailings_logs_repository import \
    MailingsLogsRepository
from api.responses.json_response import (client_deleted_successfully,
                                         raise_client_not_found)
from api.responses.success import DELETED_SUCCESSFULLY


class MailingsLogsControllers:
    def __init__(self, session):
        self.session: AsyncSession = session
        self.mailing_logs_repository = MailingsLogsRepository(session)

    def get_all(self):

        return self.mailing_logs_repository.get_all()

    def get_all_by_mailing_id(self,
                              mailing_id: int):

        return self.mailing_logs_repository.get_all_by_mailing_id(mailing_id=mailing_id)
