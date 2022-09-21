from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.schemas.message import MessageCreate
from api.controllers.message import MessageController

message_router = APIRouter(
    prefix='/messages',
    tags=['Messages'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@message_router.post('/')
@message_router.post('/', include_in_schema=False)
@managed_transaction
async def create_and_get_message(input_data: MessageCreate,
                                 session: Session = Depends(get_session),
                                 ):
    message_controller = MessageController()
    return message_controller.create_message(session=session,
                                             input_data=input_data)


@message_router.get('/{message_id}')
@message_router.get('/{message_id}/', include_in_schema=False)
async def create_and_get_message(message_id: int,
                                 session: Session = Depends(get_session),
                                 ):
    message_controller = MessageController()
    return message_controller.get_one(session=session,
                                      message_id=message_id)
