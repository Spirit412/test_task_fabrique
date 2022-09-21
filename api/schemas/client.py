from typing import ForwardRef

from api.schemas.logs.client_log import ClientLog
from api.schemas.message import MessageDB, Message
from api.schemas.message import MessageDB
from pydantic import BaseModel, Field

ClientDBWithMessages = ForwardRef("ClientDBWithMessages")


class ClientBase(BaseModel):
    phone_number: str = Field(...,
                              regex=r"^7\d{10}$",
                              description="Мобильный номер вида 7##########",
                              title="Мобильный номер вида 7##########",
                              default="79211234567",
                              )
    phone_operator_code: str = Field(...,
                                     regex=r"^\d{3}$",
                                     description="Код оператора",
                                     title="Код оператора",
                                     default="921",
                                     )
    tag: str | None = Field(None,
                            description="Тэг",
                            title="Тэг",
                            )
    timezone: str = Field(...,
                          default="Europe/Moscow",
                          description="Временная зона",
                          title="Временная зона",
                          )


class Client(ClientBase):
    id: int
    messages: list["Message"]
    logs: list["ClientLog"]


class ClientDB(ClientBase):
    id: int
    phone_number: str
    phone_operator_code: str
    tag: str

    timezone: str


class ClientDBWithMessages(ClientDB):
    messages: list["MessageDB"] | None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    phone_number: str | None
    phone_operator_code: str | None
    tag: str | None
    timezone: str | None


ClientDBWithMessages.update_forward_refs()
