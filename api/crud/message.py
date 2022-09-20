from sqlalchemy.orm import Session

from api.models import models
from api.schemas.message import MessageCreate
from api.schemas.user import User


class MessageService:

    def get_one(self, *,
                session: Session,
                id: int | None = None,
                ) -> models.Message | None:
        message = (
            session
            .query(models.Message)
        )
        message = message.filter(models.Message.id == id) if id is not None else message
        return message.one_or_none()

    def index(self, *,
              session: Session,
              ids: list[int] | None = None,
              user_id: int,
              limit: int,
              ) -> list[models.Message] | None:
        messages = (
            session
            .query(models.Message)
        )
        messages = messages.filter(models.Message.ids.in_(ids)) if ids is not None else messages
        messages = messages.filter(models.Message.user_id == user_id) if user_id is not None else messages
        return messages.limit(limit=limit).all()

    def create_message(self, *,
                       session: Session,
                       current_user: User,
                       create_data: MessageCreate,
                       ) -> models.Message | None:
        message = models.Message(
            message=create_data.message,
            user_id=current_user.id
        )
        session.add(message)
        session.flush()
        return self.get_one(session=session, id=message.id)
