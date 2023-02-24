from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


ERROR_CONNECT_DB = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Ошибка соединения с БД",
    headers={"WWW-Authenticate": "Bearer"},
)


def raise_client_not_found(client_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client ID:{client_id} not found",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_phone_number_not_acceptable(phone_number: str):
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"Номер телефона: {phone_number} не прошел валидацию.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_db_exc(msg: str):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_mailing_not_found(mailing_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Mailing ID:{mailing_id} not found",
        headers={"WWW-Authenticate": "Bearer"},
    )


def raise_message_not_found(message_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Message ID:{message_id} not found",
        headers={"WWW-Authenticate": "Bearer"},
    )


def client_deleted_successfully(client_id: int):
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Client ID:{client_id} deleted successfully",
        headers={"WWW-Authenticate": "Bearer"},
    )


def mailing_deleted_successfully(mailing_id: int):
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Mailing ID:{mailing_id} deleted successfully",
        headers={"WWW-Authenticate": "Bearer"},
    )


def message_deleted_successfully(message_id: int):
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=f"Message ID:{message_id} deleted successfully",
        headers={"WWW-Authenticate": "Bearer"},
    )
