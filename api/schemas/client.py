

from pydantic import BaseModel, Field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.schemas.message import Message  # noqa: F401
    from api.schemas.message import MessageDB  # noqa: F401
    from api.schemas.logs.client_log import ClientLog  # noqa: F401


class ClientBase(BaseModel):
    phone_number: str = Field("79211234567",
                              regex=r"^7\d{10}$",
                              description="Мобильный номер вида 7##########",
                              title="Мобильный номер вида 7##########",
                              )
    phone_operator_code: str = Field("921",
                                     regex=r"^\d{3}$",
                                     description="Код оператора",
                                     title="Код оператора",
                                     )
    tag: str | None = Field(None,
                            description="Тэг",
                            title="Тэг",
                            )
    timezone: str = Field("Europe/Moscow",
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
