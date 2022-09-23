from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from api.utils.models_utils import enum_elements_to_string
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from api.schemas.client import Client, ClientDB  # noqa: F401
    from api.schemas.logs.message_log import MessageLog  # noqa: F401
    from api.schemas.mailing import Mailing, MailingDB  # noqa: F401


class SendStatusEnum(IntEnum):
    SENT = 0
    FAIL = 1
    SUCCESS = 2


class MessageBase(BaseModel):

    send_status: int = Field(...,
                             title="Статус отправки",
                             description=f"Доступные значения:\n"
                             f"{enum_elements_to_string(SendStatusEnum)}",
                             )


class Message(MessageBase):

    id: int
    created_at: datetime

    logs: list["MessageLog"]

    mailing_id: int
    mailing: Optional["Mailing"]

    client_id: int
    client: Optional["Client"]


class MessageDB(MessageBase):
    id: int
    send_status: str
    created_at: datetime

    class Config:
        orm_mode = True


class MessageDBWithClient(MessageDB):
    client: Optional["ClientDB"]

    class Config:
        orm_mode = True


class MessageDBWithMailing(MessageDB):
    mailing: Optional["MailingDB"]

    class Config:
        orm_mode = True


class MessageDBWithAll(MessageDBWithClient, MessageDBWithMailing):
    pass


class MessageCreate(MessageBase):
    mailing_id: int
    client_id: int


class MessageUpdate(BaseModel):
    send_status: str | None = None

    mailing_id: int | None = None
    client_id: int | None = None


# MessageDBWithClient.update_forward_refs()
# MessageDBWithMailing.update_forward_refs()
# MessageDBWithAll.update_forward_refs()
