from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.sqlalchemy_connection import get_session
from api.schemas.logs.client_log import ClientLogDB
from api.schemas.logs.mailing_log import MailingLogDB
from api.schemas.logs.message_log import MessageLogDB
from api.services.logs.client_logs_repository import ClientLogsRepository
from api.services.logs.mailings_logs_repository import MailingsLogsRepository
from api.services.logs.messages_logs_repository import MessagesLogsRepository

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/clients", response_model=List[ClientLogDB])
async def get_clients_logs(session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с клиентами """
    client_logs_repository = ClientLogsRepository(session)

    db_logs = await client_logs_repository.get_all()

    return db_logs


@router.get("/clients/{client_id}", response_model=List[ClientLogDB])
async def get_client_logs(client_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с клиентом по ID клиента """
    client_logs_repository = ClientLogsRepository(session)

    db_logs = await client_logs_repository.get_all_by_client_id(client_id)

    return db_logs


@router.get("/mailings", response_model=List[MailingLogDB])
async def get_mailings_logs(session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с рассылками """
    mailing_logs_repository = MailingsLogsRepository(session)

    db_logs = await mailing_logs_repository.get_all()

    return db_logs


@router.get("/mailings/{mailing_id}", response_model=List[MailingLogDB])
async def get_mailing_logs(mailing_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с рассылкой по ID рассылки """
    mailings_logs_repository = MailingsLogsRepository(session)

    db_logs = await mailings_logs_repository.get_all_by_mailing_id(mailing_id)

    return db_logs


@router.get("/messages", response_model=List[MessageLogDB])
async def get_messages_logs(session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с сообщениями """
    messages_logs_repository = MessagesLogsRepository(session)

    db_logs = await messages_logs_repository.get_all()

    return db_logs


@router.get("/messages/{message_id}", response_model=List[MessageLogDB])
async def get_message_logs(message_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с сообщением по ID сообщения """
    messages_logs_repository = MessagesLogsRepository(session)

    db_logs = await messages_logs_repository.get_all_by_message_id(message_id)

    return db_logs