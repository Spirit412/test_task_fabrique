from api.controllers.mailings_controllers import MailingsControllers
from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.schemas.mailing import (MailingCreate, MailingDB,
                                 MailingUpdate)
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

    mailings_controllers = MailingsControllers(session)
    return mailings_controllers.get_all()


@router.get("/{mailing_id}", response_model=MailingDB)
def get_mailing(mailing_id: int,
                session: Session = Depends(get_session),
                ):
    """ Получает рассылку по ID. """

    mailings_controllers = MailingsControllers(session)
    return mailings_controllers.get_by_id(mailing_id=mailing_id)


@router.post("/", response_model=MailingDB)
@managed_transaction
def add_mailing(mailing_create: MailingCreate,
                session: Session = Depends(get_session),
                ):
    """ Добавляет рассылку. """
    mailings_controllers = MailingsControllers(session)

    return mailings_controllers.create(mailing_create=mailing_create)


@router.put("/{mailing_id}", response_model=MailingDB)
@managed_transaction
def update_mailing(mailing_id: int,
                   mailing_update: MailingUpdate,
                   session: Session = Depends(get_session),
                   ):
    """ Обновляет рассылку по ID. """

    mailings_controllers = MailingsControllers(session)
    return mailings_controllers.update(mailing_id, mailing_update)


@router.delete("/{mailing_id}")
@managed_transaction
def delete_mailing(mailing_id: int,
                   session: Session = Depends(get_session),
                   ):
    """ Удаляет рассылку по ID. """

    mailings_controllers = MailingsControllers(session)
    return mailings_controllers.delete(mailing_id=mailing_id)
