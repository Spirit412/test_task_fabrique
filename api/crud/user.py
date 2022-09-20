from sqlalchemy.orm import Session

from api.models import models
from api import schemas


class UserService:

    def get_one(self, *,
                session: Session,
                id: int | None = None,
                name: str | None = None,
                ):
        user = (
            session
            .query(models.User)
        )
        user = user.filter(models.User.id == id) if id is not None else user
        user = user.filter(models.User.name == name) if name is not None else user
        return user.one_or_none()
