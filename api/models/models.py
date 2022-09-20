import enum
from datetime import *

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, backref

from api.database.sqlalchemy_connection import Base

metadata = Base.metadata


class Mailing(Base):
    __tablename__ = 'mailings'
    id = Column(Integer, primary_key=True, index=True)
    sending_start_date = Column(DateTime(), default=None)  # Начало рассылки'
    sending_end_date = Column(DateTime(), default=None)  # Окончание рассылки
    text = Column(Text, nullable=True)
    client_filter_json = Column(Jsonb(), nullable=True)
    tag = Column(String)
    mobile_code = Column(String(length=3))

    @property
    def to_send(self):
        now = datetime.now()
        if self.start <= now <= self.end:
            return True
        else:
            return False

# для ускорения получения статистики из БД. 
# Логи разместим в разных таблицах
class Logs_Clients(Base):
    __tablename__ = 'logs_clients'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    action = Column(Integer)
    message = Column(String)
    created_at = Column(DateTime(), default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey='clients.id')

class Logs_Mailings(Base):
    __tablename__ = 'logs_mailings'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    action = Column(Integer)
    message = Column(String)
    created_at = Column(DateTime(), default=datetime.utcnow)
    mailing_id = Column(Integer, ForeignKey='mailings.id')



class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    create_sending = Column(DateTime())
    send_status = Column(Integer, nullable=False)
    client_id = ColZZZZZZZZZZZZZZZZZZZZZZZZZZZumn(Integer, ForeignKey='clients.id')
    # Можно как вариант использовать (str, enum.Enum)
    mailing_id = Column(Integer, ForeignKey='mailings.id')
    

    sending_messages_id = Column(Integer, ForeignKey('sending_messages.id'))
    clients_id = Column(Integer, ForeignKey('clients.id'))















class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password_digest = Column(String)
    data_json = Column(Jsonb(), nullable=True)









class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(length=11))  # телефонный номер 11 символов 7XXXXXXXXXX
    phone_operator_code = Column(String(length=3))  # Рассматриваем операторов с трехзначным кодом
    teg = Column(String())
    timezone = Column(String(length=3))  # +12... 0... -12
    user_id = Column(Integer, ForeignKey('users.id'))


class SendingMessage(Base):
    __tablename__ = 'sending_messages'
    id = Column(Integer, primary_key=True, index=True)
    start_sending = Column(DateTime())
    text = Column(Text())
    filter_id = Column(String())
    # Реляция. Нужно подумать
    end_sending = Column(DateTime())
