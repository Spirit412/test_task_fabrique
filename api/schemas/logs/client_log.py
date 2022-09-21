from datetime import datetime
from typing import ForwardRef

from api.schemas.client import Client, ClientDB
from api.schemas.logs.log_base import LogBase

ClientLogDB = ForwardRef("ClientLogDB")


class ClientLogBase(LogBase):
    pass


class ClientLog(ClientLogBase):
    id: int
    created_at: datetime

    client_id: int
    client: "Client" | None


class ClientLogDB(ClientLogBase):
    id: int

    client_id: int | None
    client: "ClientDB" | None


class ClientLogCreate(ClientLogBase):
    client_id: int | None


class ClientLogUpdate(ClientLogBase):
    client_id: int | None


ClientLogDB.update_forward_refs()
