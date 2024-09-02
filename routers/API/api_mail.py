from typing import Annotated

import redis
from fastapi import APIRouter, Depends, Query
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.db_dependencies import create_get_db
from sqlalchemy.orm import sessionmaker, Session
from starlette.responses import JSONResponse

from function.API.api_mail import APIMailOperate


class APIMailRouter(APIMailOperate):
    def __init__(self, module, redis_db:redis.Redis, influxdb: InfluxDB, exc,
                 db_session: sessionmaker):
        self.db_session = db_session
        APIMailOperate.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/notification/mail",
            tags=["log"],
            dependencies=[],
        )

        main_schemas = self.main_schemas
        create_schemas = self.create_schemas

        @router.on_event("startup")
        async def task_startup_event():
            db = self.db_session()
            self.initial_redis_data(db)
            db.close()

        @router.get("/history", response_model=list[main_schemas])
        async def get_history(start: Annotated[str, Query()],
                           stop: Annotated[str | None, Query()] = "",
                           ids: Annotated[list[str] | None, Query()] = None,
                           status: Annotated[list[str] | None, Query()] = None,
                           senders: Annotated[list[str] | None, Query()] = None,
                           ):
            return JSONResponse(content=self.get_history(start, stop, ids, status, senders))

        @router.post("/send")
        async def create_logs(mail: create_schemas,
                              db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                content = await self.create_mails(mail, db)
                return JSONResponse(content=content)

        @router.post("/send_without_return")
        async def create_logs(mail: create_schemas,
                              db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                content = await self.create_mails_without_return(mail, db)
                return JSONResponse(content=content)

        @router.get("/test")
        async def test_log():
            return JSONResponse(content="test")

        @router.get("/test2")
        async def test_log2():
            raise self.exc(status_code=444, message="test exception", message_code=5)

        return router
