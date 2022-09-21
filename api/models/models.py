import enum
from datetime import *

from api.database.sqlalchemy_connection import Base
from fastapi.encoders import jsonable_encoder
from sqlalchemy import (DECIMAL, JSON, Boolean, Column, Date, DateTime, Enum,
                        ForeignKey, Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import backref, relationship

metadata = Base.metadata


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(length=11))  # телефонный номер 11 символов 7XXXXXXXXXX
    phone_operator_code = Column(String(length=3), default="921")  # Рассматриваем операторов с трехзначным кодом
    teg = Column(String())
    timezone = Column(String(), default="Europe/Moscow")  # +12... 0... -12

    # RELLATION
    messages = relationship("Message", back_populates="client", lazy="dynamic")
    logs = relationship("ClientLog", back_populates="client", lazy="dynamic")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(), default=datetime.utcnow)
    send_status = Column(Integer, nullable=False)
    # FOR RELATION
    mailing_id = Column(Integer, ForeignKey("mailings.id"))
    mailing = relationship("Mailing", back_populates="messages", lazy="dynamic")

    clients_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="messages", lazy="dynamic")

    logs = relationship("Logs_Messages", back_populates="messages", lazy="dynamic")


class Mailing(Base):
    __tablename__ = "mailings"
    id = Column(Integer, primary_key=True, index=True)
    sending_start_date = Column(DateTime(), default=None)  # Начало рассылки"
    sending_end_date = Column(DateTime(), default=None)  # Окончание рассылки
    message_text = Column(Text, nullable=True)
    client_filter_json = Column(JSONB, default={})


# # # # # # # # # # # # # # LOGS  # # # # # # # # # # # # # # #

# Общие поля в отдельный класс
class LoggerLevelsEnum(enum.Enum):
    DEBUG = 0
    INFO = 1
    ERROR = 2
    WARNING = 3


class LoggerActionsEnum(enum.Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    REQUEST = 4


class LoggingBase():
    level = Column(Enum(LoggerLevelsEnum), nullable=False)
    action = Column(Enum(LoggerActionsEnum), nullable=False)
    message_text = Column(String)
    data_json = Column(JSONB, default={})
    created_at = Column(DateTime(), default=datetime.utcnow)


class Logs_Mailings(Base, LoggingBase):
    __tablename__ = "logs_mailings"
    id = Column(Integer, primary_key=True, index=True)
    mailing_id = Column(Integer, ForeignKey("mailings.id"))


class Logs_Clients(Base, LoggingBase):
    __tablename__ = "logs_clients"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))


class Logs_Messages(Base, LoggingBase):
    __tablename__ = "logs_messages"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
