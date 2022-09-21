from re import search
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.database.sqlalchemy_async_connection import get_async_session
from api.auth.auth import get_user_db
from api.factories.message import MessageFactory

message_router = APIRouter(
    prefix='/messages',
    tags=['Messages'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@message_router.post('/')
@message_router.post('/', include_in_schema=False)
@managed_transaction
async def create_and_get_message(input_data: schemas.MessageCreate,
                                 session: Session = Depends(get_async_session),
                                 current_user=Depends(get_user_db),
                                 ):

    return message_factory.create_message(session=session,
                                          current_user=current_user,
                                          input_data=input_data)
