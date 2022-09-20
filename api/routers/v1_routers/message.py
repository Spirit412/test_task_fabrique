from re import search
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import schemas
from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.auth.auth import get_current_user
from api.factories.message import MessageFactory

message_router = APIRouter(
    prefix='/messages',
    tags=['Messages'],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)


@message_router.post('/', response_model=schemas.MessageDB | list[schemas.MessageDB])
@message_router.post('/', response_model=schemas.MessageDB | list[schemas.MessageDB], include_in_schema=False)
@managed_transaction
async def create_and_get_message(input_data: schemas.MessageCreate,
                                 session: Session = Depends(get_session),
                                 current_user=Depends(get_current_user),
                                 ):
    """
    **Записать сообщение**

    Сервер слушает и отвечает в какой-нибудь эндпоинт, в него на вход поступают данные в формате json:
    Сообщения клиента-пользователя:

    <CODE>{
        name:       "имя отправителя",
        message:    "текст сообщение"
    }</CODE>

    В заголовках указан Bearer токен, полученный из эндпоинта выше (между Bearer и полученным токеном должно быть нижнее подчеркивание).
    Проверить токен, в случае успешной проверки токена, полученное сообщение сохранить в БД.

    **Если** пришло сообщение вида:

    <CODE>{
        name:       "имя отправителя",
        message:    "history 10"
    }</CODE>

    проверить токен, в случае успешной проверки токена отправить отправителю 10 последних сообщений из БД

    Добавить описание и инструкцию по запуску и комментарии в коде, если изменяете формат сообщений, то подробное описание ендпоинтов и их полей.
    """
    # Из ТЗ, сделал вывод что POST запрос должен выполнять б.логику на создание или получение сообщений. Это неправильно с точки зрения REST API.
    # В ТЗ везде указано "name: 'имя отправителя'". Т.е. текущий пользователь создаёт сообщения для себя и их же может получить.
    # Не описана ситуация отправитель->получатель

    message_factory = MessageFactory()
    if bool(search('^history\s+\d+', input_data.message)):
        return message_factory.index(session=session,
                                     current_user=current_user,
                                     input_data=input_data)
    return message_factory.create_message(session=session,
                                          current_user=current_user,
                                          input_data=input_data)
