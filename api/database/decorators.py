import functools
import inspect

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.database.sqlalchemy_connection import get_session


def managed_transaction(func):
    """Простой декоратор для роутов для с транзакциями. 
    Если HTTPException, то rollback. Иначе commit"""
    @functools.wraps(func)
    async def wrap_func(*args, session: Session = Depends(get_session), **kwargs):
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(*args, session=session, **kwargs)
            else:
                result = func(*args, session=session, **kwargs)
            session.commit()
        except HTTPException as e:
            session.rollback()
            raise e
        return result

    return wrap_func