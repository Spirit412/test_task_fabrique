from datetime import datetime

from api.schemas.logs.log_base import LogBase
from pydantic import BaseModel, Field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.schemas.mailing import Mailing  # noqa: F401
    from api.schemas.mailing import MailingDB  # noqa: F401


class MailingLogBase(LogBase):
    pass


class MailingLog(MailingLogBase):
    id: int
    created_at: datetime = Field(datetime.utcnow(),
                                 )

    mailing_id: int | None
    mailing: "Mailing"


class MailingLogDB(MailingLogBase):
    id: int
    mailing_id: int | None
    mailing: "MailingDB"


class MailingLogCreate(MailingLogBase):
    mailing_id: int | None


class MailingLogUpdate(MailingLogBase):
    mailing_id: int | None
