from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from api.database.async_session import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncSession:
    session = async_session()
    try:
        async with async_session() as session:
            yield session
    except HTTPException:
        session.rollback()
        raise
    finally:
        session.close()


Base: DeclarativeMeta = declarative_base()


# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
