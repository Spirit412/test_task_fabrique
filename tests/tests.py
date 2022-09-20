import pytest
from fastapi.testclient import TestClient

# Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.main import app

from api.database.sqlalchemy_connection import get_session, Base

# Import logger and sys for format log in console
import sys
import json
from loguru import logger

from faker import Faker

# Import ENV
from config import settings

# Format logger messages
fmt = "<green>{time}</green> - {name} - {level} - {message}"
logger.add(sys.stderr, format=fmt, filter="my_module", level="INFO", backtrace=True,
           diagnose=True, colorize=True)

fake = Faker(locale="ru_RU")

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DBNAME}'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine,
                                   )


# Session fixture
@pytest.fixture()
def session():
    # если требуется очистить БД
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

# client fixture


@pytest.fixture()
def client(session):
    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_db

    yield TestClient(app)


HEADERS = {"accept": "application/json",
           "Content-Type": "application/x-www-form-urlencoded",
           }
ME: dict = {}


def test_create_user(client):
    name = fake.first_name()
    logger.info(f"name: name")
    payload = {"name": name,
               "password": name,
               }
    r = client.post("v1/users/login", headers=HEADERS, data=payload)
    logger.info(f"Ответ: {r.json()}")
    logger.info(f"Ответ: {r.status_code}")
    logger.info(f"Ответ: {r.json()}")
    global TOKEN
    TOKEN = r.json()["token"]
    logger.info(f"token: {TOKEN}")
    assert r.status_code == 200


def test_me(client):
    HEADERS["Authorization"] = "Bearer " + TOKEN
    r = client.get("v1/users/me", headers=HEADERS)
    assert r.status_code == 200
    ME.update(r.json())

    logger.info(f"Ответ: {ME}")
    # Проверка наличия ключей
    assert "id" in ME.keys()


# PYTEST команда: python -m pytest -v -s -l tests/tests.py
