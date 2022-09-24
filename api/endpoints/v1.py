from api.endpoints.v1_routers import clients, logs, mailings, messages
from fastapi import APIRouter

v1_router = APIRouter(
    prefix='/v1',
    tags=[],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)

v1_router.include_router(clients.router)
# v1_router.include_router(mailings.router)
# v1_router.include_router(messages.router)
v1_router.include_router(logs.router)
