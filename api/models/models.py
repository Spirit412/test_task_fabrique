import enum
from datetime import *
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseUserTable
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID, JSONB

from api.database.sqlalchemy_connection import Base
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
metadata = Base.metadata


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: list[OAuthAccount] = relationship("OAuthAccount", lazy="joined")


class Logs_Mailings(Base):
    __tablename__ = 'logs_mailings'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    action = Column(Integer)
    message = Column(String)
    data_json = Column(JSONB)
    created_at = Column(DateTime(), default=datetime.utcnow)

    mailing_id = Column(Integer, ForeignKey('mailings.id'))


class Logs_Clients(Base):
    __tablename__ = 'logs_clients'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    action = Column(Integer)
    message = Column(String)
    data_json = Column(JSONB)
    created_at = Column(DateTime(), default=datetime.utcnow)

    client_id = Column(Integer, ForeignKey('clients.id'))


class Logs_Messages(Base):
    __tablename__ = 'logs_messages'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    action = Column(Integer)
    message = Column(String)
    data_json = Column(JSONB)
    created_at = Column(DateTime(), default=datetime.utcnow)

    message_id = Column(Integer, ForeignKey('messages.id'))


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(length=11))  # телефонный номер 11 символов 7XXXXXXXXXX
    phone_operator_code = Column(String(length=3))  # Рассматриваем операторов с трехзначным кодом
    teg = Column(String())
    timezone = Column(String(length=3))  # +12... 0... -12


class Mailing(Base):
    __tablename__ = 'mailings'
    id = Column(Integer, primary_key=True, index=True)
    sending_start_date = Column(DateTime(), default=None)  # Начало рассылки'
    sending_end_date = Column(DateTime(), default=None)  # Окончание рассылки
    message_text = Column(Text, nullable=True)
    client_filter_json = Column(JSONB, default={}, nullable=True)
    mobile_code = Column(String(length=3))

    @property
    def to_send(self):
        if self.sending_start_date <= datetime.now() <= self.sending_end_date:
            return True
        else:
            return False


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime())
    send_status = Column(Integer, nullable=False)

    mailing_id = Column(Integer, ForeignKey('mailings.id'))
    clients_id = Column(Integer, ForeignKey('clients.id'))


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password_digest = Column(String)
