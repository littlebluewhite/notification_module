from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from general_operator.app.SQL.database import SQLDB
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.app.redis_db.redis_db import RedisDB
from general_operator.function.exception import GeneralOperatorException
from general_util.log.deal_log import DealSystemLog
from redis.client import Redis

from app.SQL import models
from data.API import api_mail
from routers.API.api_mail import APIMailRouter

# from fastapi.security.api_key import APIKeyHeader

from version import version


def create_connection(config):
    redis_db = RedisDB(config.redis.to_dict()).redis_client()
    db = SQLDB(config.sql.to_dict())
    models.Base.metadata.create_all(bind=db.get_engine())
    influxdb = InfluxDB(config.influxdb.to_dict())
    return db, redis_db, influxdb


def create_app(db: SQLDB, redis_db: Redis, influxdb: InfluxDB, server_config: dict):
    app = FastAPI(title="notification", version=version)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    db_session = db.new_db_session()

    app.include_router(APIMailRouter(
        module=api_mail, redis_db=redis_db, influxdb=influxdb, exc=GeneralOperatorException,
        db_session=db_session).create())

    @app.middleware("http")
    async def deal_with_log(request: Request, call_next):
        if server_config["system_log_enable"]:
            response = await call_next(request)
            await DealSystemLog(request=request, response=response,
                                url_mapping=None, code_rules=None).deal(server_config["system_log_g_server"])
            return response

    @app.exception_handler(GeneralOperatorException)
    async def unicorn_exception_handler(request: Request, exc: GeneralOperatorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"{exc.message}", "message_code": f"{exc.message_code}"},
            headers={"message": f"{exc.message}", "message_code": f"{exc.message_code}"}
        )

    @app.get("/exception")
    async def test_exception():
        raise GeneralOperatorException(status_code=423, detail="test exception")

    return app
