from api.auth.auth import AuthService
from api.models import models
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.schemas.user import *
from api.crud.user import UserService
from api.responses.exceptions import EXCEPTION_USER_EXISTS


class UserFactory:

    def create_user(self, *,
                    session: Session,
                    user: UserCreate,
                    ) -> models.User | HTTPException:
        self.validate(session=session, user=user)
        user_service = AuthService()
        return user_service.create_user(session=session,
                                        user_data=user,
                                        )

    def validate(self, *,
                 session: Session,
                 user: UserCreate,
                 ) -> models.User | HTTPException:
        user_service = UserService()
        if user_service.get_one(session=session, name=user.name) is not None:
            raise EXCEPTION_USER_EXISTS
