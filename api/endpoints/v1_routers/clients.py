from api.controllers.client_controllers import ClientControllers
from api.database.sqlalchemy_async_connection import get_session
from api.schemas.client import ClientCreate, ClientDB, ClientUpdate
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ClientDB])
def get_clients(session: AsyncSession = Depends(get_session),
                ):
    """ Получает список всех клиентов. """

    client_controllers = ClientControllers(session)
    return client_controllers.get_all()


@router.get("/{client_id}", response_model=ClientDB)
def get_client(client_id: int,
               session: AsyncSession = Depends(get_session),
               ):
    """ Получает клиента по ID. """

    client_controllers = ClientControllers(session)
    return client_controllers.get_by_id(get_by_id=client_id)


@router.post("/")
def add_client(client_create: ClientCreate,
               session: AsyncSession = Depends(get_session),
               ):
    """ Добавляет клиента. """

    client_controllers = ClientControllers(session)
    return client_controllers.create(model_create=client_create)


@router.put("/{client_id}", response_model=ClientDB)
def update_client(client_id: int,
                  client_update: ClientUpdate,
                  session: AsyncSession = Depends(get_session),
                  ):
    """ Обновляет клиента по ID. """

    client_controllers = ClientControllers(session)
    return client_controllers.update(client_id=client_id,
                                     client_update=client_update,
                                     )


@router.delete("/{client_id}")
def delete_client(client_id: int,
                  session: AsyncSession = Depends(get_session),
                  ):
    """ Удаляет клиента по ID. """

    client_controllers = ClientControllers(session)
    return client_controllers.delete(client_id=client_id,
                                     )
