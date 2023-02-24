import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api.endpoints.v1 import v1_router

from .custom_logging import CustomizeLogger

logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("logging_config.json")


tags_metadata = [
    {
        "name": "Logs",
        "description": "Получение логов",
    },
    {
        "name": "Clients",
        "description": "Редактирование клиентов"
    },
    {
        "name": "Mailings",
        "description": "Редактирование рассылок"
    },
    {
        "name": "Messages",
        "description": "Просмотр отправленных сообщений"
    }
]

description = """ API для администрирования рассылками.
"""


app = FastAPI(
    logger=CustomizeLogger.make_logger(config_path),
    openapi_tags=tags_metadata,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    root_path="/v1/"
)

app.logger = logger

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/v1/openapi.json")
def get_openapi_json(request: Request):
    return JSONResponse(get_openapi(
        title="API",
        version="1.0.0",
        description="**openapi.json тестового задания**",
        routes=app.routes
    ))
