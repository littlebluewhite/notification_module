from typing import Annotated

import redis
from fastapi import APIRouter, Depends, Query
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.db_dependencies import create_get_db
from sqlalchemy.orm import sessionmaker, Session
from starlette.responses import JSONResponse

import data.notify
from function.operate.notify import NotifyOperate


class APINotifyRouter:
    def __init__(self, redis_db: redis.Redis, influxdb: InfluxDB, exc,
                 db_session: sessionmaker):
        self.db_session = db_session
        self.notify_operate = NotifyOperate(data.notify, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/notification/notify",
            tags=["notify"],
            dependencies=[],
        )

        main_schemas = self.notify_operate.main_schemas
        create_schemas = self.notify_operate.create_schemas

        @router.get("/history", response_model=list[main_schemas])
        async def get_history(start: Annotated[str, Query()],
                              stop: Annotated[str | None, Query()] = "",
                              ids: Annotated[list[str] | None, Query()] = None,
                              senders: Annotated[list[str] | None, Query()] = None,
                              ):
            return JSONResponse(content=self.notify_operate.get_history(start, stop, ids, senders))

        @router.post("/send")
        async def send_notify(notify: create_schemas,
                              db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                content = await self.notify_operate.create_notify(notify, db)
                return JSONResponse(content=content)

        @router.post("/send_without_return")
        async def send_email_without_return(
                notify: create_schemas, db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                content = await self.notify_operate.create_notify_without_return(notify, db)
                return JSONResponse(content=content)

        return router
