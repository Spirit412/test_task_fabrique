from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database.decorators import managed_transaction
from api.database.sqlalchemy_connection import get_session
from api.factories.user import UserFactory
from api.routers.v1_routers.user import user_router
from api.routers.v1_routers.message import message_router
from api.schemas.token import Token
from api.schemas.user import UserCreate

v1_router = APIRouter(
    prefix='/v1',
    tags=[],
    dependencies=[],
    responses={404: {'description': 'Not found'}},
)

v1_router.include_router(user_router)
v1_router.include_router(message_router)


@v1_router.post('/signup', response_model=Token)
@v1_router.post('/signup/', include_in_schema=False, response_model=Token)
@managed_transaction
async def signup(user: UserCreate,
                 session: Session = Depends(get_session),
                 user_factory: UserFactory = Depends(),
                 ):
    access_token = user_factory.create_user(session=session, user=user)
    return {"token": access_token}
