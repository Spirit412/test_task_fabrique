from datetime import datetime
from enum import IntEnum
from typing import ForwardRef
from api.schemas.client import Client, ClientDB
from api.schemas.logs.message_log import MessageLog
from api.schemas.mailing import Mailing, MailingDB

from api.utils.utils import enum_elements_to_string
from pydantic import BaseModel, Field

MessageDBWithClient = ForwardRef("MessageDBWithClient")
MessageDBWithMailing = ForwardRef("MessageDBWithMailing")
MessageDBWithAll = ForwardRef("MessageDBWithAll")


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
    mailing: "Mailing" | None

    client_id: int
    client: "Client" | None


class MessageDB(MessageBase):
    id: int
    send_status: str
    created_at: datetime


class MessageDBWithClient(MessageDB):
    client: "ClientDB" | None


class MessageDBWithMailing(MessageDB):
    mailing: "MailingDB" | None


class MessageDBWithAll(MessageDBWithClient, MessageDBWithMailing):
    pass


class MessageCreate(MessageBase):
    mailing_id: int
    client_id: int


class MessageUpdate(BaseModel):
    send_status: str | None

    mailing_id: str | None
    client_id: str | None


MessageDBWithClient.update_forward_refs()
MessageDBWithMailing.update_forward_refs()
MessageDBWithAll.update_forward_refs()
