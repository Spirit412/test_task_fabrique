import enum
from datetime import *

from api.database.sqlalchemy_connection import Base
from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

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
    # RELLATION
    logs = relationship("MessageLog", back_populates="messages", lazy="dynamic")

    mailing_id = Column(Integer, ForeignKey("mailings.id"))
    mailing = relationship("Mailing", back_populates="messages", lazy="dynamic")

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="messages", lazy="dynamic")


class Mailing(Base):
    __tablename__ = "mailings"
    id = Column(Integer, primary_key=True, index=True)
    sending_start_date = Column(DateTime(), default=None)  # Начало рассылки"
    sending_end_date = Column(DateTime(), default=None)  # Окончание рассылки
    message_text = Column(Text, nullable=True)
    client_filter_json = Column(JSONB, default={})
    # RELLATION
    messages = relationship("Message", back_populates="mailings", lazy="dynamic")
    logs = relationship("MailingLog", back_populates="mailings", lazy="dynamic")


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


class LogBase():
    level = Column(Enum(LoggerLevelsEnum), nullable=False)
    action = Column(Enum(LoggerActionsEnum), nullable=False)
    message_text = Column(String)
    data_json = Column(JSONB, default={})
    created_at = Column(DateTime(), default=datetime.utcnow)


class MailingLog(Base, LogBase):
    __tablename__ = "logs_mailings"
    id = Column(Integer, primary_key=True, index=True)
    mailing_id = Column(Integer, ForeignKey("mailings.id"))


class ClientLog(Base, LogBase):
    __tablename__ = "logs_clients"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    # RELLATION
    client = relationship("Client", back_populates="logs_clients", lazy="dynamic")


class MessageLog(Base, LogBase):
    __tablename__ = "logs_messages"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    # RELLATION
