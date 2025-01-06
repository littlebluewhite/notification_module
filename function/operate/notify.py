import asyncio
import json
import threading

import influxdb_client
from general_operator.function.General_operate import GeneralOperate
import data.mail

from function.operate.mail import MailOperate


class NotifyFunction:
    pass


class NotifyOperate(GeneralOperate):
    def __init__(self, module, redis_db, influxdb, exc):
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)
        self.mailOperate = MailOperate(data.mail, redis_db, influxdb, exc)
        self.messageOperate = None
        self.lineOperate = None

    def get_history(self, start, stop, ids: list, senders: list):
        stop_str = ""
        id_str = ""
        sender_str = ""

        if stop:
            stop_str = f", stop: {stop}"
        if ids:
            id_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.id == "{_id}"''' for _id in ids]) + ")"
            id_str += combine
        if senders:
            sender_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.sender == "{sender}"''' for sender in senders]) + ")"
            sender_str += combine
        stmt = f'''from(bucket:"notification")
|> range(start: {start}{stop_str})
{sender_str}
{id_str}
|> filter(fn:(r) => r._measurement == "notify")
|> filter(fn:(r) => r._field == "data")'''
        d = self.query(stmt)
        result = []
        for table in d:
            for record in table.records:
                result.append(json.loads(record["_value"]))

        return result

    async def create_notify(self, notify_create, db):
        sql_list = self.create_sql(db, [dict()])
        notify = self.main_schemas(
            id=sql_list[0].id, sender=notify_create.sender, subject=notify_create.subject,
            message=notify_create.message, timestamp=sql_list[0].created_at.timestamp(),
            is_email=notify_create.is_email, is_message=notify_create.is_message, is_line=notify_create.is_line)

        return await self.deal_notify(notify, notify_create)

    async def create_notify_without_return(self, notify_create, db):
        sql_list = self.create_sql(db, [dict()])
        notify = self.main_schemas(
            id=sql_list[0].id, sender=notify_create.sender, subject=notify_create.subject,
            message=notify_create.message, timestamp=sql_list[0].created_at.timestamp(),
            is_email=notify_create.is_email, is_message=notify_create.is_message, is_line=notify_create.is_line)

        thread = threading.Thread(target=self.thread_target, args=(notify, notify_create))
        thread.start()
        return "ok"

    def thread_target(self, notify, notify_create):
        asyncio.run(self.deal_notify(notify, notify_create))

    async def deal_notify(self, notify, notify_create):
        tasks = []
        task_names = []

        if notify.is_email:
            mail_create = self.create_schemas(
                sender=notify.sender, subject=notify.subject, message=notify.message,
                groups=notify_create.groups, accounts=notify_create.accounts, emails=notify_create.emails)
            tasks.append(self.mailOperate.create_mail_without_db(mail_create))
            task_names.append("email")
        if notify.is_message:
            # tasks.append(self.messageOperate.create_message())
            # task_names.append("message")
            pass
        if notify.is_line:
            # tasks.append(self.lineOperate.create_line())
            # task_names.append("line")
            pass

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # deal with results
        response = {}
        for name, result in zip(task_names, results):
            if isinstance(result, Exception):
                response[name] = {"success": False, "data": {}, "error": str(result)}
            else:
                response[name] = {"success": True, "data": result, "error": ""}

        notify.email_result = response.get("email", None)
        notify.message_result = response.get("message", None)
        notify.line_result = response.get("line", None)

        # write to influxdb
        points = [influxdb_client.Point(
            "notify").tag("id", str(notify.id))
                  .tag("sender", str(notify.sender))
                  .time(int(notify.timestamp * 10 ** 6) * 1000)
                  .field("data", str(notify.json())
                         )]
        self.write(points)
        print("send notify success")
        return notify.dict()
