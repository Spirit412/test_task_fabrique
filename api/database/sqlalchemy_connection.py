from fastapi import HTTPException
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from api.database.session import Session


def get_session():
    session = Session()
    try:
        yield session
    except HTTPException:
        session.rollback()
        raise
    finally:
        session.close()


Base = declarative_base()
