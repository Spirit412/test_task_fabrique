from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.schemas.message import Message, MessageDB, MessageDBWithAll
from api.services.messages_repository import MessagesRepository
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[MessageDB])
def get_messages(session: Session = Depends(get_session),
                 ):
    """ Получает все сообщения. """
    messages_repository = MessagesRepository(session)

    db_messages = messages_repository.get_all()

    return db_messages


@router.get("/{message_id}", response_model=MessageDBWithAll, responses={'404': {'model': Message}})
def get_message(message_id: int,
                session: Session = Depends(get_session),
                ):
    """ Получает сообщение по ID. """
    message_repository = MessagesRepository(session)

    db_message: Optional[Message] = message_repository.get_by_id(message_id)
    if db_message is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{message_id}] Message not found"})

    return db_message


@router.delete("/{message_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
@managed_transaction
def delete_message(message_id: int,
                   session: Session = Depends(get_session),
                   ):
    """ Удаляет сообщение по ID. """
    logger = Logger(session)
    message_repository = MessagesRepository(session)

    db_message: Optional[Message] = message_repository.get_by_id(message_id)
    if db_message is None:
        logger.create_message_log(None,
                                  LoggerLevelsEnum.error,
                                  LoggerActionsEnum.delete,
                                  f"[ID:{message_id}] Message Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{message_id}] Message not found"})

    message_repository.delete(db_message)
    message_repository.commit()

    logger.create_message_log(None,
                              LoggerLevelsEnum.debug,
                              LoggerActionsEnum.delete,
                              f"[ID:{message_id}] Message Deleted")

    return JSONResponse(status_code=200, content={'message': f'[ID:{message_id}] Message deleted successfully'})
