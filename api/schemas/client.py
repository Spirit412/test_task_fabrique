from __future__ import annotations
from doctest import REPORT_ONLY_FIRST_FAILURE
from pydantic import BaseModel, Field, root_validator
import phonenumbers
from phonenumbers import NumberParseException
from phonenumbers import carrier
from typing import TYPE_CHECKING, Optional
from api.responses.json_response import raise_phone_number_not_acceptable
if TYPE_CHECKING:
    from api.schemas.message import Message, MessageDB  # noqa: F401
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
    tag: str = Field(...,
                     description="Тэг",
                     title="Тэг",
                     )
    timezone: str = Field("Europe/Moscow",
                          description="Временная зона",
                          title="Временная зона",
                          )


class ClientBaseCreateUpdate(BaseModel):
    phone_number: str = Field("79211234567",
                              regex=r"^7\d{10}$",
                              description="Мобильный номер вида 7##########",
                              title="Мобильный номер вида 7##########",
                              )

    tag: str = Field(...,
                     description="Тэг",
                     title="Тэг",
                     )
    timezone: str = Field("Europe/Moscow",
                          description="Временная зона",
                          title="Временная зона",
                          )

    @root_validator
    def validate_fields(cls, values):
        string_number = values.get('phone_number')
        try:

            phone_parse = phonenumbers.parse(string_number, region='RU')
        except NumberParseException:
            raise_phone_number_not_acceptable(string_number)

        if phonenumbers.is_valid_number(phone_parse) is False:
            raise_phone_number_not_acceptable(string_number)

        values['phone_number'] = phonenumbers.normalize_digits_only(phone_parse)
        # свой формат номера
        values['phone_operator_code'] = str(phone_parse.national_number)[:3]
        # # Из номера берем код оператора  и заполняем phone_operator_code
        return values


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

    class Config:
        orm_mode = True


class ClientDBWithMessages(ClientDB):
    messages: Optional[list["MessageDB"]]

    class Config:
        orm_mode = True


class ClientCreate(ClientBaseCreateUpdate):
    pass


class ClientUpdate(ClientBaseCreateUpdate):
    pass


from api.schemas.message import Message, MessageDB  # noqa: F401, E402, F811
from api.schemas.logs.client_log import ClientLog  # noqa: F401, E402, F811

ClientDBWithMessages.update_forward_refs()
