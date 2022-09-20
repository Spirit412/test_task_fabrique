from api import models, schemas
from api.crud.message import MessageService
from api.models import models
from sqlalchemy.orm import Session

from api.responses import exceptions


class MessageFactory:

    def create_message(self, *,
                       session: Session,
                       current_user: schemas.User,
                       input_data: schemas.MessageCreate,
                       ) -> models.Message | None:
        if input_data.name != current_user.name:
            exceptions.raise_user_create_message()
        message_service = MessageService()
        return message_service.create_message(session=session,
                                              current_user=current_user,
                                              create_data=input_data,
                                              )

    def get_one(self, *,
                session: Session,
                message_id: int
                ) -> models.Message | None:
        message_service = MessageService()
        return message_service.get_one(session=session,
                                       id=message_id)

    def index(self, *,
              session: Session,
              current_user: schemas.User,
              input_data: schemas.MessageCreate,
              ) -> list[models.Message] | None:
        if input_data.name != current_user.name:
            exceptions.raise_user_create_message()
        message_service = MessageService()
        limit: int = input_data.message.split()[1]
        return message_service.index(session=session,
                                     user_id=current_user.id,
                                     limit=limit,
                                     )
