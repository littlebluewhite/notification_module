from typing import Annotated

import redis
from fastapi import APIRouter, Depends, Query
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.dependencies.db_dependencies import create_get_db
from sqlalchemy.orm import sessionmaker, Session
from starlette.responses import JSONResponse
import data.mail
from function.operate.mail import MailOperate

class APIMailRouter:
    def __init__(self, redis_db:redis.Redis, influxdb: InfluxDB, exc,
                 db_session: sessionmaker):
        self.db_session = db_session
        self.mail_operate = MailOperate(data.mail, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix="/api/notification/mail",
            tags=["mail"],
            dependencies=[],
        )

        main_schemas = self.mail_operate.main_schemas
        create_schemas = self.mail_operate.create_schemas

        @router.get("/history", response_model=list[main_schemas])
        async def get_history(start: Annotated[str, Query()],
                           stop: Annotated[str | None, Query()] = "",
                           ids: Annotated[list[str] | None, Query()] = None,
                           status: Annotated[list[str] | None, Query()] = None,
                           senders: Annotated[list[str] | None, Query()] = None,
                           ):
            return JSONResponse(content=self.mail_operate.get_history(start, stop, ids, status, senders))

        @router.post("/send")
        async def send_email(mail: create_schemas,
                              db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                content = await self.mail_operate.create_mail(mail, db)
                return JSONResponse(content=content)

        @router.post("/send_without_return")
        async def send_email_without_return(mail: create_schemas,
                              db: Session = Depends(create_get_db(self.db_session))):
            with db.begin():
                content = await self.mail_operate.create_mail_without_return(mail, db)
                return JSONResponse(content=content)

        return router
