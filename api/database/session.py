import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.config import settings
from api.responses.json_response import ERROR_CONNECT_DB

# LOGGING DB логгер БД
db_log_file_name = Path.cwd() / 'api/sqlalchemy.log'
db_log_level = logging.INFO

db_log_formatter = logging.Formatter(fmt='\n%(asctime)s - %(levelname)s\n QUERY:\n %(message)s\n')

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_log_level)
db_handler.setFormatter(db_log_formatter)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)

try:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DBNAME}'

    alchemy_engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )

    Session = sessionmaker(autocommit=False,
                           autoflush=False,
                           expire_on_commit=False,
                           bind=alchemy_engine,
                           )
except Exception as e:
    ERROR_CONNECT_DB
