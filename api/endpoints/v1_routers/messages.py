from api.controllers.messages_controllers import MessagesControllers
from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.schemas.message import MessageDB, MessageDBWithAll
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

    messages_controllers = MessagesControllers(session)
    return messages_controllers.get_all()


@router.get("/{message_id}", response_model=MessageDBWithAll)
def get_message(message_id: int,
                session: Session = Depends(get_session),
                ):
    """ Получает сообщение по ID. """

    messages_controllers = MessagesControllers(session)
    return messages_controllers.get_by_id(message_id=message_id)


@router.delete("/{message_id}")
@managed_transaction
def delete_message(message_id: int,
                   session: Session = Depends(get_session),
                   ):
    """ Удаляет сообщение по ID. """

    messages_controllers = MessagesControllers(session)
    return messages_controllers.delete(message_id=message_id)
