from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


ERROR_CONNECT_DB = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Ошибка соединения с БД',
    headers={"WWW-Authenticate": "Bearer"},
)


def raise_client_not_found(client_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client ID:{client_id} not found",
        headers={"WWW-Authenticate": "Bearer"},
    )


def client_deleted_successfully(client_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client ID:{client_id} deleted successfully",
        headers={"WWW-Authenticate": "Bearer"},
    )
