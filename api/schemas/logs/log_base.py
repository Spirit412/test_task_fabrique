from enum import IntEnum

from api.utils.utils import enum_elements_to_string
from pydantic import BaseModel, Field


class LoggerLevelsEnum(IntEnum):
    DEBUG = 0
    INFO = 1
    ERROR = 2
    WARNING = 3


class LoggerActionsEnum(IntEnum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    REQUEST = 4


class LogBase(BaseModel):
    level: int = Field(...,
                       title="Уровень лога", description=f"Доступные значения:\n"
                       f"{enum_elements_to_string(LoggerLevelsEnum)}",
                       )
    action: int = Field(...,
                        title="Тип действия",
                        description=f"Доступные значения:\n"
                        f"{enum_elements_to_string(LoggerActionsEnum)}",
                        )
    message_text: str = Field("No Message",
                              title="Текст лога",
                              )
    data_json: dict = Field(dict(error="Example Text"),
                            title="Json строка с дополнительными данными к логу",
                            )


class LogUpdateBase(BaseModel):
    level: int | None
    action: int | None
    message_text: str | None
    data_json: str | None
