from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.routers.v1_routers.message import message_router

v1_router = APIRouter(
    prefix='/v1',
    tags=[],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)

v1_router.include_router(message_router)
