from fastapi import HTTPException, status

###################   AUTH   ###################


EXCEPTION_PASSWORD = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials. Password verification not passed.",
    headers={"WWW-Authenticate": "Bearer"}
)

EXCEPTION_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad token.",
    headers={"WWW-Authenticate": "Bearer"}
)

EXCEPTION_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired. Get new one.",
    headers={"WWW-Authenticate": "Bearer"}
)

EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"}
)


EXCEPTION_USER_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with this name already exists.",
    headers={"WWW-Authenticate": "Bearer"}
)
"""Пользователь с таким именем уже существует"""


def raise_validation_error(field: str):
    """Поле {field} не прошло валидацию."""
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Поле {field} не прошло валидацию.",
        headers={"WWW-Authenticate": "Bearer"}
    )


###################   SQLALCHEMY   ###################

def raise_sqlalchemy(message: str):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f'Ошибка БД: {message}',
        headers={"WWW-Authenticate": "Bearer"}
    )


ERROR_CONNECT_DB = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Ошибка соединения с БД',
    headers={"WWW-Authenticate": "Bearer"}
)

USER_NOT_EXISTS = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User is not exists',
    headers={"WWW-Authenticate": "Bearer"}
)


def raise_user_create_message():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Пользователь с данным токеном не может создать сообщение под чужим пользователем',
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_logic_exception(message: str):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"}
    )
