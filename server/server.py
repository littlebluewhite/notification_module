import grpc
from general_operator.app.SQL.database import SQLDB
from general_operator.app.influxdb.influxdb import InfluxDB
from general_operator.function.exception import GeneralOperatorException
from redis import Redis
from sqlalchemy.orm import sessionmaker

import data.mail
import data.notify
from function.operate.mail import MailOperate
from function.operate.notify import NotifyOperate
from schemas.notify import NotifyCreate
from server.proto import notification_pb2, notification_pb2_grpc
from schemas.mail import MailCreate


class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def __init__(self, db: SQLDB, redis_db: Redis, influxdb: InfluxDB):
        self.db_session: sessionmaker = db.new_db_session()
        self.mail_operate = MailOperate(data.mail, redis_db, influxdb, GeneralOperatorException)
        self.notify_operate = NotifyOperate(data.notify, redis_db, influxdb, GeneralOperatorException)

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
        # db = self.db_session()
        # with db.begin():
        response: dict = await self.mail_operate.create_mail_without_db(mail_create)
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
        # db.close()
        return result

    async def SendEmailSimple(self, request, context):
        mail_create = MailCreate(
            sender=request.sender,
            subject=request.subject,
            message=request.message,
            groups=request.groups,
            accounts=request.accounts,
            emails=request.emails
        )
        print("receive request: ", mail_create)
        # db = self.db_session()
        # with db.begin():
        response: str = await self.mail_operate.create_mails_without_db_return(mail_create)
        result = notification_pb2.SimpleMessageResponse(
            message=response
        )
        # db.close()
        return result

    async def SendNotify(self, request, context):
        notify_create = NotifyCreate(
            sender=request.sender,
            subject=request.subject,
            message=request.message,
            is_email=request.is_email,
            is_message=request.is_message,
            is_line=request.is_line,
            groups=request.groups,
            accounts=request.accounts,
            emails=request.emails
        )
        print("Received SendNotify request:", notify_create)

        try:
            # get database session
            db = self.db_session()
            with db.begin():
                # use NotifyOperate deal notify
                notify_response = await self.notify_operate.create_notify(notify_create, db)
                email_result = notify_response["email_result"]["success"] if notify_response["email_result"] else False
                message_result = notify_response["message_result"]["success"] if notify_response["message_result"] else False
                line_result = notify_response["line_result"]["success"] if notify_response["line_result"] else False

                result = notification_pb2.NotifyResponse(
                    id=notify_response["id"],
                    sender=notify_response["sender"],
                    subject=notify_response["subject"],
                    message=notify_response["message"],
                    is_email=notify_response["is_email"],
                    is_message=notify_response["is_message"],
                    is_line=notify_response["is_line"],
                    email_result=email_result,
                    message_result=message_result,
                    line_result=line_result,
                    timestamp=notify_response["timestamp"]
                )
                return result
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return notification_pb2.NotifyResponse()

    async def SendNotifySimple(self, request, context):
        notify_create = NotifyCreate(
            sender=request.sender,
            subject=request.subject,
            message=request.message,
            is_email=request.is_email,
            is_message=request.is_message,
            is_line=request.is_line,
            groups=request.groups,
            accounts=request.accounts,
            emails=request.emails
        )
        print("Received SendNotifySimple request:", notify_create)

        try:
            # get database session
            db = self.db_session()
            with db.begin():
                # use NotifyOperate to deal simple notify
                response = await self.notify_operate.create_notify_without_return(notify_create, db)

                result = notification_pb2.SimpleMessageResponse(
                    message=response
                )
                return result
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return notification_pb2.SimpleMessageResponse()
