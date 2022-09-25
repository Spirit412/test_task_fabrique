from __future__ import annotations
from datetime import datetime

from api.schemas.logs.log_base import LogBase
from pydantic import BaseModel, Field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.schemas.message import Message, MessageDB  # noqa: F401


class MessageLogBase(LogBase):
    pass


class MessageLog(MessageLogBase):
    id: int
    created_at: datetime = Field(datetime.utcnow(),
                                 )

    message_id: int | None
    message: "Message"

    class Config:
        orm_mode = True


class MessageLogDB(MessageLogBase):
    id: int

    message_id: int | None
    message: "MessageDB"

    class Config:
        orm_mode = True


class MessageLogCreate(MessageLogBase):
    message_id: int | None


class MessageLogUpdate(MessageLogBase):
    message_id: int | None


from api.schemas.message import Message, MessageDB  # noqa: F401, E402, F811

MessageLogDB.update_forward_refs()
