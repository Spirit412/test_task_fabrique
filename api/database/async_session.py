# import logging
# import os
# from pathlib import Path

# from api.config import settings
# from api.responses.exceptions import ERROR_CONNECT_DB
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker

# # LOGGING DB логгер БД
# db_log_file_name = Path.cwd() / 'api/sqlalchemy.log'
# db_log_level = logging.INFO

# db_log_formatter = logging.Formatter(fmt='\n%(asctime)s - %(levelname)s\n QUERY:\n %(message)s\n')

# db_handler = logging.FileHandler(db_log_file_name)
# db_handler.setLevel(db_log_level)
# db_handler.setFormatter(db_log_formatter)

# db_logger = logging.getLogger('sqlalchemy')
# db_logger.addHandler(db_handler)

# try:
#     SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DBNAME}'
#     engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

#     async def get_async_session() -> AsyncSession:
#         async_session = sessionmaker(
#             engine, class_=AsyncSession, expire_on_commit=False
#         )
#         async with async_session() as session:
#             yield session

# except Exception as e:
#     ERROR_CONNECT_DB
