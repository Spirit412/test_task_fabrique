from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import sessionmaker

from api.config import settings

from .db_url_builder import DbUrlEnvBuilder, DbUrlParams

# Проверяем наличие папки "logs" в корне. Если нет, создаём
if settings.APP_DEBUG:
    db_log_file_name = Path.cwd() / "logs"
    db_log_file_name.mkdir(parents=True, exist_ok=True)
    #

    db_log_file_name = Path.cwd() / "logs" / "sqlalchemy.log"
    db_log_level = logging.INFO

    db_log_formatter = logging.Formatter(
        fmt="\n%(asctime)s - %(levelname)s\n QUERY:\n %(message)s\n")

    db_handler = RotatingFileHandler(filename=db_log_file_name, maxBytes=1 * 1024 * 1024,
                                     backupCount=5)  # Ограничение файла журнала 1Мб. всего 5 файлов. Дальше по циклу.
    db_handler.setLevel(db_log_level)
    db_handler.setFormatter(db_log_formatter)

    db_logger = logging.getLogger("sqlalchemy")
    db_logger.addHandler(db_handler)

ENV_MAPPING = {
    DbUrlParams.PROTOCOL: "DB_PROTOCOL",
    DbUrlParams.DRIVER: "DB_DRIVER",
    DbUrlParams.USER: "DB_USER",
    DbUrlParams.PASSWORD: "DB_PASSWORD",
    DbUrlParams.HOST: "DB_HOST",
    DbUrlParams.PORT: "DB_PORT",
    DbUrlParams.DBNAME: "DB_DBNAME",
}
DbUriBuilderLocal = DbUrlEnvBuilder.get_local_type(ENV_MAPPING)


class AsyncSessionManager:
    def __init__(self) -> None:
        self.async_engine: AsyncEngine | Engine | None = None  # type: ignore
        self.refresh()

    def __new__(cls: type[AsyncSessionManager]) -> AsyncSessionManager:
        # sort-of singleton
        if not hasattr(cls, "instance"):
            cls.instance = super(AsyncSessionManager, cls).__new__(cls)
        return cls.instance

    def refresh(self):
        os.environ["DB_DRIVER"] = "asyncpg"
        sql_db_url = DbUriBuilderLocal().from_env().to_str()
        # Принудительно подключаем драйвер asyncpg независимо от DB_DRIVER
        # sql_db_url = DbUriBuilderLocal().from_env().driver("asyncpg")
        self.async_engine = create_async_engine(sql_db_url,
                                                echo=settings.APP_DEBUG,
                                                poolclass=AsyncAdaptedQueuePool,
                                                future=True,
                                                )

    @property
    async def AsyncSessionLocal(self) -> async_sessionmaker:
        return await async_sessionmaker(bind=self.async_engine,
                                        class_=AsyncSession,
                                        expire_on_commit=False,
                                        autoflush=True,
                                        autocommit=False,
                                        future=True,
                                        )

    @property
    def alchemy_engine(self) -> AsyncEngine:
        return self.async_engine


# SessionForCelery - Для Celery. Если использовать SessionManager().alchemy_engine в целери таск не проходит, ругается на ошибку
# sessionmaker нет query
AsyncSessionForCelery = async_sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=AsyncSessionManager().alchemy_engine,
                                           expire_on_commit=False,
                                           future=True,
                                           )

__all__ = ["AsyncSessionManager", "DbUriBuilderLocal", "AsyncSessionForCelery"]
