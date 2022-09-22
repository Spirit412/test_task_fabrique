from api import models
from api.schemas.message import MessageCreate
from api.services.messages_repository import MessagesRepository
from api.models import models
from sqlalchemy.orm import Session

from api.responses import exceptions


class MessageController:

    def create_message(self, *,
                       session: Session,
                       input_data: MessageCreate,
                       ) -> models.Message | None:

        message_service = MessagesRepository()
        return message_service.create(session=session,
                                      schemas_create=input_data,
                                      )

    def get_one(self, *,
                session: Session,
                message_id: int,
                ) -> models.Message | None:
        message_service = MessagesRepository()
        return message_service.get_by_id(session=session,
                                       model_id=message_id)
