
from general_operator.app.SQL.database import SQLDB
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.function.exception import GeneralOperatorException
from redis import Redis
from sqlalchemy.orm import sessionmaker

import data.API.api_mail
from server.proto import notification_pb2, notification_pb2_grpc
from function.API.api_mail import APIMailOperate
from schemas.API.api_mail import MailCreate


class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def __init__(self, db: SQLDB, redis_db: Redis, influxdb: InfluxDB):
        self.db_session: sessionmaker = db.new_db_session()
        self.api_mail_operate = APIMailOperate(data.API.api_mail, redis_db, influxdb, GeneralOperatorException)
    async def SendEmail(self, request, context):
        mail_create = MailCreate(
            sender=request.sender,
            subject=request.subject,
            message=request.message,
            groups=request.groups,
            accounts=request.accounts,
            emails=request.emails
        )
        print("receive request: ", mail_create)
        db = self.db_session()
        with db.begin():
            response: dict = await self.api_mail_operate.create_mails(mail_create, db)
            result = notification_pb2.EmailSendResponse(
                id=response["id"],
                sender="Alarm",
                subject=response["subject"],
                message=response["message"],
                status=response["status"],
                recipients=[notification_pb2.Recipient(group=r["group"], accounts=[
                    notification_pb2.Account(username=a["username"], email=a["email"], name=a["name"]) for a in r["account"]
                ]) for r in response["recipient"]],
                timestamp=response["timestamp"]
            )
        db.close()
        return result
