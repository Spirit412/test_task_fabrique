from api.schemas.logs.client_log import (ClientLog, ClientLogCreate,
                                         ClientLogUpdate)
from api.utils.models_utils import update_model
from sqlalchemy.orm import Session, joinedload


class ClientLogsRepository:

    async def get_all(self, *,
                      session: Session,
                      ) -> list[ClientLog]:
        query = select(ClientLog).options(selectinload(ClientLog.client))
        execute = await self.session.execute(query)

        db_models: list[ClientLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, *,
                        session: Session,
                        model_id: int,
                        ) -> ClientLog | None:
        query = select(ClientLog).where(ClientLog.id == model_id).options(selectinload(ClientLog.client))
        execute = await self.session.execute(query)

        db_model: ClientLog | None = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_client_id(self, *,
                                   session: Session,
                                   client_id: int,
                                   ) -> list[ClientLog]:
        query = select(ClientLog).where(ClientLog.client_id == client_id).options(selectinload(ClientLog.client))
        execute = await self.session.execute(query)

        db_models: list[ClientLog] = execute.scalars().all()
        return db_models

    def create(self, *,
               session: Session,
               model_create: ClientLogCreate,
               ) -> ClientLog:
        db_model = ClientLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, *,
               session: Session,
               db_model: ClientLog,
               model_update: ClientLogUpdate,
               ) -> ClientLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, *,
                     session: Session,
                     db_model: ClientLog,
                     ) -> None:
        await self.session.delete(db_model)
