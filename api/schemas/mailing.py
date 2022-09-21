from api.schemas.logs.mailing_log import MailingLog
from api.schemas.message import MessageDB, Message
from datetime import datetime
from typing import ForwardRef
from pydantic import BaseModel, Field
from datetime import datetime

MailingDBWithMessages = ForwardRef("MailingDBWithMessages")


class FilterJson(BaseModel):
    tag: str | None = Field(None,
                            description="Тэг",
                            title="Тэг",
                            )
    phone_operator_code: str | None = Field(None,
                                            regex=r"^\d{3}$",
                                            description="Код оператора",
                                            title="Код оператора",
                                            default="921",
                                            )


class MailingBase(BaseModel):

    sending_start_date: datetime = Field(...,
                                         default=datetime.utcnow(),
                                         title="Дата начала рассылки",
                                         description="Временную зона UTC",
                                         )
    sending_end_date: datetime = Field(...,
                                       default=datetime.utcnow(),
                                       title="Дата окончания рассылки",
                                       description="Временную зона UTC",
                                       )

    message_text: str = Field(...,
                              default="Example Message",
                              title="Сообщение которое будет отправляться клиентам",
                              )
    client_filter_json: FilterJson = Field(...,
                                           default={},
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
    client_filter_json: str


class MailingDBWithMessages(MailingDB):
    messages: list["MessageDB"] | None


class MailingCreate(MailingBase):
    pass


class MailingUpdate(BaseModel):
    sending_start_date: datetime
    sending_end_date: datetime

    message_text: str | None
    client_filter_json: FilterJson | None


MailingDBWithMessages.update_forward_refs()
