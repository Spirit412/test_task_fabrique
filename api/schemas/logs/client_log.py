from __future__ import annotations
from datetime import datetime
# from typing import ForwardRef

from api.schemas.logs.log_base import LogBase

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.schemas.client import Client, ClientDB  # noqa: F401
    from api.schemas.logs.log_base import LogBase  # noqa: F401


class ClientLogBase(LogBase):
    pass


class ClientLog(ClientLogBase):
    id: int
    created_at: datetime

    client_id: int
    client: "Client"

    class Config:
        orm_mode = True


class ClientLogDB(ClientLogBase):
    id: int

    client_id: int | None
    client: "ClientDB"

    class Config:
        orm_mode = True


class ClientLogCreate(ClientLogBase):
    client_id: int | None


class ClientLogUpdate(ClientLogBase):
    client_id: int | None


from api.schemas.client import Client, ClientDB  # noqa: F401, E402, F811
from api.schemas.logs.log_base import LogBase  # noqa: F401, E402, F811

ClientLogDB.update_forward_refs()
