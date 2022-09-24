from api.controllers.clients_logs_controllers import ClientLogsControllers
from api.controllers.mailings_logs_controllers import MailingsLogsControllers
from api.controllers.messages_logs_controllers import MessagesLogsControllers
from api.database.sqlalchemy_connection import get_session
from api.schemas.logs.client_log import ClientLogDB
from api.schemas.logs.mailing_log import MailingLogDB
from api.schemas.logs.message_log import MessageLogDB
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/clients", response_model=list[ClientLogDB])
def get_clients_logs(session: Session = Depends(get_session),
                     ):
    """ Получает все логи операций с клиентами """

    client_logs_controllers = ClientLogsControllers(session)
    return client_logs_controllers.get_all()


@router.get("/clients/{client_id}", response_model=list[ClientLogDB])
def get_client_logs(client_id: int,
                    session: Session = Depends(get_session),
                    ):
    """ Получает все логи операций с клиентом по ID клиента """

    client_logs_controllers = ClientLogsControllers(session)
    return client_logs_controllers.get_all_by_client_id(client_id=client_id)


@router.get("/mailings", response_model=list[MailingLogDB])
def get_mailings_logs(session: Session = Depends(get_session),
                      ):
    """ Получает все логи операций с рассылками """

    mailing_logs_controllers = MailingsLogsControllers(session)
    return mailing_logs_controllers.get_all()


@router.get("/mailings/{mailing_id}", response_model=list[MailingLogDB])
def get_mailing_logs(mailing_id: int,
                     session: Session = Depends(get_session),
                     ):
    """ Получает все логи операций с рассылкой по ID рассылки """

    mailings_logs_controllers = MailingsLogsControllers(session)
    return mailings_logs_controllers.get_all_by_mailing_id(mailing_id=mailing_id)


@router.get("/messages", response_model=list[MessageLogDB])
def get_messages_logs(session: Session = Depends(get_session),
                      ):
    """ Получает все логи операций с сообщениями """

    messages_logs_controllers = MessagesLogsControllers(session)
    return messages_logs_controllers.get_all()


@router.get("/messages/{message_id}", response_model=list[MessageLogDB])
def get_message_logs(message_id: int,
                     session: Session = Depends(get_session),
                     ):
    """ Получает все логи операций с сообщением по ID сообщения """

    messages_logs_controllers = MessagesLogsControllers(session)
    return messages_logs_controllers.get_all_by_mailing_id(message_id=message_id)
