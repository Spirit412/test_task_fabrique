from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.schemas.mailing import (Mailing, MailingCreate, MailingDB,
                                 MailingUpdate)
from api.services.mailings_repository import MailingsRepository
from api.utils.logger_util import Logger, LoggerActionsEnum, LoggerLevelsEnum
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/mailings",
    tags=["Mailings"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[MailingDB])
def get_mailings(session: Session = Depends(get_session),
                 ):
    """ Получает все рассылки. """
    mailings_repository = MailingsRepository(session)

    db_mailings = mailings_repository.get_all()

    return db_mailings


@router.get("/{mailing_id}", response_model=MailingDB)
def get_mailing(mailing_id: int, session: Session = Depends(get_session),
                ):
    """ Получает рассылку по ID. """
    mailings_repository = MailingsRepository(session)

    db_mailing: Mailing | None = mailings_repository.get_by_id(mailing_id)
    if db_mailing is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{mailing_id}] Mailing not found"})

    return db_mailing


@router.post("/", response_model=MailingDB)
@managed_transaction
def add_mailing(client_create: MailingCreate, session: Session = Depends(get_session),
                ):
    """ Добавляет рассылку. """
    
    logger = Logger(session)
    mailings_repository = MailingsRepository(session)

    db_mailing = mailings_repository.create(client_create)

    mailings_repository.commit()
    mailings_repository.refresh(db_mailing)

    logger.create_mailing_log(db_mailing.id,
                              LoggerLevelsEnum.debug,
                              LoggerActionsEnum.create,
                              f"[ID:{db_mailing.id}] Mailing Created")

    return db_mailing


@router.put("/{mailing_id}", response_model=MailingDB)
@managed_transaction
def update_mailing(mailing_id: int,
                   mailing_update: MailingUpdate,
                   session: Session = Depends(get_session),
                   ):
    """ Обновляет рассылку по ID. """
    
    logger = Logger(session)
    mailings_repository = MailingsRepository(session)

    db_mailing: Mailing | None = mailings_repository.get_by_id(mailing_id)
    if db_mailing is None:
        logger.create_mailing_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.delete,
                                  f"[ID:{mailing_id}] Mailing Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{mailing_id}] Client not found"})

    db_mailing = mailings_repository.update(db_mailing, mailing_update)

    logger.create_mailing_log(db_mailing.id, LoggerLevelsEnum.debug, LoggerActionsEnum.update,
                              f"[ID:{mailing_id}] Mailing Updated")

    return db_mailing


@router.delete("/{mailing_id}")
@managed_transaction
def delete_mailing(mailing_id: int, session: Session = Depends(get_session),
                   ):
    """ Удаляет рассылку по ID. """
    
    logger = Logger(session)
    mailings_repository = MailingsRepository(session)

    db_mailing: Mailing | None = mailings_repository.get_by_id(mailing_id)
    if db_mailing is None:
        logger.create_mailing_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.delete,
                                  f"[ID:{mailing_id}] Mailing Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{mailing_id}] Mailing not found"})

    logger.create_mailing_log(None, LoggerLevelsEnum.debug, LoggerActionsEnum.delete,
                              f"[ID:{mailing_id}] Mailing Deleted")

    return JSONResponse(status_code=200, content={'message': f'[ID:{mailing_id}] Mailing deleted successfully'})
