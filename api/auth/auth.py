from datetime import datetime, timedelta
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from api.database.sqlalchemy_connection import get_session
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session
from api.schemas.schemas import *
from api.config import settings
from api.crud.token import TokenService
from api.models import models
from api.responses import exceptions
from api.crud.user import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class AuthService:
    TIME_LIFE_TOKEN = 5  # минуты

    @classmethod
    def verify_password(cls,
                        plain_password,
                        hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password) -> str:
        return pwd_context.hash(password)

    @classmethod
    def create_access_token(cls,
                            user: models.User,
                            ) -> set:
        user_data = schemas.UserDB.from_orm(user)
        payload = {
            'name': user_data.name,
            'iat': datetime.utcnow()
        }
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.user_service = UserService()
        self.token_service = TokenService()

    def verify_token(self,
                     token: str = Depends(oauth2_scheme)) -> models.User | HTTPException:
        """
        Верификация токена
        """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if 'name' in payload:
                name: str = payload.get('name')
                if name is None:
                    raise exceptions.EXCEPTION_TOKEN
            if 'iat' in payload:
                iat: datetime = payload.get('iat')
                iat_datetime = datetime.fromtimestamp(iat)  # Приводим секунды к формату даты
                if (iat_datetime + timedelta(minutes=self.TIME_LIFE_TOKEN)) < datetime.now():  # ошибка если дата.время создания токена+дельта < меньше текущей дата.время
                    raise exceptions.EXCEPTION_TOKEN_EXPIRED
        except JWTError as e:
            raise exceptions.EXCEPTION_TOKEN
        try:
            user = self.user_service.get_one(session=self.session,
                                             name=name)
        except ValidationError as e:
            raise exceptions.EXCEPTION_TOKEN
        return user

    def authenticate_user(self,
                          name: str,
                          password: str) -> models.User | HTTPException:

        user = self.user_service.get_one(session=self.session,
                                         name=name)
        if not user:
            raise exceptions.EXCEPTION
        if not self.verify_password(password, user.password_digest):
            raise exceptions.EXCEPTION_PASSWORD
        return user

    def create_user(self,
                    session: Session,
                    user_data: UserCreate,
                    ):
        """
        Создание пользователя
        """
        user = models.User(name=user_data.name,
                           password_digest=self.get_password_hash(user_data.password),
                           )
        session.add(user)
        session.flush()
        return self.create_access_token(user)


def get_current_user(token: str = Depends(oauth2_scheme),
                     auth_service: AuthService = Depends(),
                     ) -> User:
    user_model = auth_service.verify_token(token=token)
    return User.from_orm(user_model)
