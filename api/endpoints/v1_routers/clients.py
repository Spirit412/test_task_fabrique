from api.controllers.client_controllers import ClientControllers
from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.schemas.client import Client, ClientCreate, ClientDB, ClientUpdate
from api.services.clients_repository import ClientsRepository
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ClientDB])
def get_clients(session: Session = Depends(get_session),
                ):
    """ Получает список всех клиентов. """
    client_controllers = ClientControllers(session)

    return client_controllers.get_all()


@router.get("/{client_id}", response_model=ClientDB)
def get_client(client_id: int,
               session: Session = Depends(get_session),
               ):
    """ Получает клиента по ID. """
    client_controllers = ClientControllers(session)

    return client_controllers.get_by_id(get_by_id=client_id)


@ router.post("/", response_model=ClientDB)
@managed_transaction
def add_client(client_create: ClientCreate,
               session: Session = Depends(get_session),
               ):
    """ Добавляет клиента. """
    client_controllers = ClientControllers(session)

    return client_controllers.create(model_create=client_create)


@ router.put("/{client_id}", response_model=ClientDB)
@managed_transaction
def update_client(client_id: int,
                  client_update: ClientUpdate,
                  session: Session = Depends(get_session),
                  ):
    """ Обновляет клиента по ID. """
    logger = Logger(session)
    clients_repository = ClientsRepository(session)

    db_client: Optional[Client] = clients_repository.get_by_id(client_id)
    if db_client is None:
        logger.create_client_log(None,
                                 LoggerLevelsEnum.ERROR,
                                 LoggerActionsEnum.UPDATE,
                                 f"[ID:{client_id}] Client Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{client_id}] Client not found"})

    db_client = clients_repository.update(db_client, client_update)

    clients_repository.commit()
    clients_repository.refresh(db_client)

    logger.create_client_log(db_client.id,
                             LoggerLevelsEnum.DEBUG,
                             LoggerActionsEnum.UPDATE,
                             f"[ID:{client_id}] Client Updated")

    return db_client


@router.delete("/{client_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
@managed_transaction
def delete_client(client_id: int, session: Session = Depends(get_session),
                  ):
    """ Удаляет клиента по ID. """
    logger = Logger(session)
    clients_repository = ClientsRepository(session)

    db_client: Optional[Client] = clients_repository.get_by_id(client_id)
    if db_client is None:
        logger.create_client_log(None, LoggerLevelsEnum.ERROR, LoggerActionsEnum.DELETE,
                                 f"[ID:{client_id}] Client Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{client_id}] Client not found"})

    clients_repository.delete(db_client)
    clients_repository.commit()

    logger.create_client_log(None, LoggerLevelsEnum.DEBUG, LoggerActionsEnum.DELETE,
                             f"[ID:{client_id}] Client Deleted")

    return JSONResponse(status_code=200, content={'message': f'[ID:{client_id}] Client deleted successfully'})
