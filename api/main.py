import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import json
from api.config import settings
from api.routers.v1 import v1_router
from .costum_logging import CustomizeLogger
from fastapi.exceptions import RequestValidationError, ValidationError

logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("logging_config.json")

app = FastAPI(
    logger=CustomizeLogger.make_logger(config_path),
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


# Глобальный обработчик ошибок схем Pydantic входящих запросов. 
# Меняем аид/формат ответа
@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    print(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    # response = {"message": [], "data": None}
    response = {"message": []}
    for error in exc_json:
        response['message'].append(error['loc'][-1] + f": {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get("/v1/openapi.json")
async def get_openapi_json(request: Request):
    return JSONResponse(get_openapi(
        title="API",
        version="1.0.0",
        description="**Апи тестового задания**",
        routes=app.routes
    ))

app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, "SECRET"),
    prefix="/auth/google",
    tags=["auth"],
)