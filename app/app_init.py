from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from general_operator.app.SQL.database import SQLDB
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.app.redis_db.redis_db import RedisDB
from general_operator.function.exception import GeneralOperatorException
from general_operator.routers.all_table import AllTableRouter
from general_util.log.deal_log import DealSystemLog
from redis.client import Redis

import data
from app.SQL import models
from data.log.log_mapping import url_mapping
from routers.API.mail.main import APIMailRouter
from routers.API.notify.main import APINotifyRouter


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
        redis_db=redis_db, influxdb=influxdb, exc=GeneralOperatorException,
        db_session=db_session).create())

    app.include_router(APINotifyRouter(
        redis_db=redis_db, influxdb=influxdb, exc=GeneralOperatorException,
        db_session=db_session).create())

    app.include_router(AllTableRouter(
        module=data, redis_db=redis_db, influxdb=influxdb,
        exc=GeneralOperatorException, db_session=db_session,
        is_initial=True).create())

    @app.middleware("http")
    async def deal_with_log(request: Request, call_next):
        request_body = ""
        if server_config["system_log_enable"]:
            request_body = await request.body()
            request_body = request_body.decode()
            async def receive():
                return {
                    "type": "http.request",
                    "body": request_body,
                    "more_body": False
                }
            # 重建request
            request = Request(
                scope=request.scope,
                receive=receive
            )
        try:
            response = await call_next(request)
        except Exception as e:
            print(e)
            response = JSONResponse(status_code=500, content={"error": str(e)},
                                    headers={"message": str(e), "message_code": "500"})
        try:
            if server_config["system_log_enable"]:
                response_body = b"".join([chunk async for chunk in response.body_iterator]).decode()
                await DealSystemLog(request=request, response=response, request_body=request_body,
                                    response_body=response_body, url_mapping=url_mapping,
                                    code_rules=None).deal(server_config["system_log_g_server"])
                # 重建response
                response = Response(content=response_body,
                                    status_code=response.status_code,
                                    headers=response.headers)
        except Exception as e:
            print(e)
        return response

    @app.exception_handler(GeneralOperatorException)
    async def unicorn_exception_handler(request: Request, exc: GeneralOperatorException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"{exc.message}", "message_code": f"{exc.message_code}"},
            headers={"message": f"{exc.message}", "message_code": f"{exc.message_code}"}
        )

    return app
