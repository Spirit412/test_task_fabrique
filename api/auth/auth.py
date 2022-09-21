from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.database.sqlalchemy_async_connection import get_async_session
from passlib.context import CryptContext

from api.models import models


from fastapi import Depends
from fastapi_users.db import (SQLAlchemyUserDatabase)
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, models.User, models.OAuthAccount)
