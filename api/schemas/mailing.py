from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, Field

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from api.schemas.message import Message, MessageDB  # noqa: F401
    from api.schemas.logs.mailing_log import MailingLog  # noqa: F401


class FilterJson(BaseModel):
    tag: str | None = Field(None,
                            description="Тэг",
                            title="Тэг",
                            )
    phone_operator_code: str | None = Field("921",
                                            regex=r"^\d{3}$",
                                            description="Код оператора",
                                            title="Код оператора",
                                            )


class MailingBase(BaseModel):

    sending_start_date: datetime = Field(datetime.utcnow(),
                                         title="Дата начала рассылки",
                                         description="Временную зона UTC",
                                         )
    sending_end_date: datetime = Field(datetime.utcnow(),
                                       title="Дата окончания рассылки",
                                       description="Временную зона UTC",
                                       )

    message_text: str = Field("Example Message",
                              title="Сообщение которое будет отправляться клиентам",
                              )
    client_filter_json: FilterJson = Field({},
                                           title="Json фильтра по которому будут выбираться клиенты",
                                           )


class Mailing(MailingBase):
    id: int
    messages: list["Message"]
    logs: list["MailingLog"]


class MailingDB(MailingBase):
    id: int
    sending_start_date: datetime
    sending_end_date: datetime

    message_text: str
    client_filter_json: FilterJson

    class Config:
        orm_mode = True


class MailingDBWithMessages(MailingDB):
    messages: list["MessageDB"] | None


class MailingCreate(MailingBase):
    pass


class MailingUpdate(BaseModel):
    sending_start_date: datetime
    sending_end_date: datetime

    message_text: str | None
    client_filter_json: FilterJson | None


from api.schemas.message import Message, MessageDB  # noqa: F401, E402, F811
from api.schemas.logs.mailing_log import MailingLog  # noqa: F401, E402, F811

MailingDBWithMessages.update_forward_refs()
