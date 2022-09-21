from datetime import datetime
from typing import TYPE_CHECKING

from api.schemas.logs.log_base import LogBase
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from api.schemas.message import Message  # noqa: F401
    from api.schemas.message import MessageDB  # noqa: F401


class MessageLogBase(LogBase):
    pass


class MessageLog(MessageLogBase):
    id: int
    created_at: datetime = Field(datetime.utcnow(),
                                 )

    message_id: int | None
    message: "Message"


class MessageLogDB(MessageLogBase):
    id: int

    message_id: int | None
    message: "MessageDB"


class MessageLogCreate(MessageLogBase):
    message_id: int | None


class MessageLogUpdate(MessageLogBase):
    message_id: int | None
