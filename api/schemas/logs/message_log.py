from api.schemas.message import Message, MessageDB
from datetime import datetime
from typing import List, Optional
from typing import ForwardRef
from api.schemas.logs.log_base import LogBase
from pydantic import BaseModel, Field

MessageLogDB = ForwardRef("MessageLogDB")


class MessageLogBase(LogBase):
    pass


class MessageLog(MessageLogBase):
    id: int
    created_at: datetime = Field(...,
                                 default=datetime.utcnow(),
                                 )

    message_id: int | None
    message: "Message" | None


class MessageLogDB(MessageLogBase):
    id: int

    message_id: int | None
    message: "MessageDB" | None


class MessageLogCreate(MessageLogBase):
    message_id: int | None


class MessageLogUpdate(MessageLogBase):
    message_id: int | None


MessageLogDB.update_forward_refs()
