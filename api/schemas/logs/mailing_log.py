from datetime import datetime
from typing import ForwardRef

from api.schemas.logs.log_base import LogBase
from api.schemas.mailing import Mailing, MailingDB
from pydantic import BaseModel, Field

MailingLogDB = ForwardRef("MailingLogDB")


class MailingLogBase(LogBase):
    pass


class MailingLog(MailingLogBase, table=True):
    id: int
    created_at: datetime = Field(...,
                                 default=datetime.utcnow(),
                                 )

    mailing_id: int | None
    mailing: "Mailing" | None


class MailingLogDB(MailingLogBase):
    id: int
    mailing_id: int | None
    mailing: "MailingDB" | None


class MailingLogCreate(MailingLogBase):
    mailing_id: int | None


class MailingLogUpdate(MailingLogBase):
    mailing_id: int | None


MailingLogDB.update_forward_refs()
