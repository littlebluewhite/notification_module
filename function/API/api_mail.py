import csv
import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

from general_operator.function.General_operate import GeneralOperate
import influxdb_client
from general_util.async_request import fetch
from general_util.config_manager import ConfigManager

from schemas.API.api_mail import Status, Recipient, Account


class APIMailFunction:
    def __init__(self):
        pass

    @staticmethod
    def send_email(email: list, subject: str, message: str, sender: str):
        try:
            with smtplib.SMTP(ConfigManager.server.smtp_server) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(ConfigManager.server.smtp_user, ConfigManager.server.smtp_password)
                cc = []
                bcc = []
                msg = MIMEText(message, "plain", "utf-8")
                msg.preamble = subject
                msg["Subject"] = subject
                msg['From'] = formataddr((str(Header(sender, 'utf-8')), "your-email@example.com"))
                msg["To"] = ", ".join(email)
                if len(cc): msg["Cc"] = ", ".join(cc)
                if len(bcc): msg["Bcc"] = ", ".join(bcc)
                response = smtp.send_message(msg)
                if response:
                    return False
                else:
                    return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_account_data():
        urls = [f"{ConfigManager.server.account_server}/api/account/get_all_account_list_table",
                f"{ConfigManager.server.account_server}/api/account/get_all_account_info_list_table"]
        data = await fetch(urls, headers={"Authorization": f"Bearer {ConfigManager.server.super_token}"})
        return data[0], data[1]

    @staticmethod
    def change_account_group_to_recipient(create_group: list, create_account: list, create_email: list,
                                          account_list, account_info):
        to_email = []
        recipient = []
        user_dict = {list(item.keys())[0]: list(item.values())[0] for item in account_info.values()}
        for g in create_group:
            accounts = []
            for _id, a in account_list.items():
                if list(a.values())[0]["Group"] == g:
                    username = list(a.keys())[0]
                    email = list(list(account_info[_id].values())[0].values())[0]["e-mail"]
                    if email not in to_email:
                        to_email.append(email)
                    name = list(list(account_info[_id].values())[0].values())[0]["Name"]
                    accounts.append({"username": username, "email": email, "name": name})
            recipient.append({"group": g, "account": accounts})
        for a in create_account:
            info = user_dict.get(a, None)
            if info is not None:
                email = list(info.values())[0]["e-mail"]
                username = a
                name = list(info.values())[0]["Name"]
                if email not in to_email:
                    to_email.append(email)
                recipient.append(
                    {"group": "", "account": [{"username": username, "email": email, "name": name}]})
        mails = []
        for e in create_email:
            mails.append(e)
            if e not in to_email:
                to_email.append(e)

        recipient.append({"group": "", "account": [{"username": "", "email": e, "name": ""} for e in mails]})
        recipient_pydantic = [
            Recipient(
                group=r["group"],
                account=[
                    Account(username=a["username"], email=a["email"], name=a["name"]) for a in r["account"]
                ]
            ) for r in recipient
        ]
        return to_email, recipient_pydantic


csv.field_size_limit(10 ** 7)


class APIMailOperate(GeneralOperate, APIMailFunction):
    def __init__(self, module, redis_db, influxdb, exc):
        GeneralOperate.__init__(self, module, redis_db, influxdb, exc)

    def get_history(self, start, stop, ids: list, status: list, senders: list):
        stop_str = ""
        id_str = ""
        status_str = ""
        sender_str = ""

        if stop:
            stop_str = f", stop: {stop}"
        if ids:
            id_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.id == "{_id}"''' for _id in ids]) + ")"
            id_str += combine
        if status:
            status_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.status == "{s}"''' for s in status]) + ")"
            status_str += combine
        if senders:
            sender_str = f"""|> filter(fn:(r) => """
            combine = " or ".join([f'''r.sender == "{sender}"''' for sender in senders]) + ")"
            sender_str += combine
        stmt = f'''from(bucket:"notification")
|> range(start: {start}{stop_str})
{status_str}
{sender_str}
{id_str}
|> filter(fn:(r) => r._measurement == "mail")
|> filter(fn:(r) => r._field == "data")'''
        d = self.query(stmt)
        result = []
        for table in d:
            for record in table.records:
                result.append(json.loads(record["_value"]))

        return result

    async def create_mails(self, mail_create, db) -> dict:
        # write to sql and get id
        sql_list = self.create_sql(db, [dict()])
        mail = self.main_schemas(id=sql_list[0].id, sender=mail_create.sender, subject=mail_create.subject,
                                 message=mail_create.message, timestamp=sql_list[0].created_at.timestamp(),
                                 recipient=[])

        # get account and group email
        account_list, account_info = await self.get_account_data()

        # deal with group and account
        to_email, recipient = self.change_account_group_to_recipient(
            create_group=mail_create.groups, create_account=mail_create.accounts, create_email=mail_create.emails,
            account_list=account_list, account_info=account_info)

        # send mail
        is_success = self.send_email(email=to_email, subject=mail.subject, message=mail.message, sender=mail.sender)
        if is_success:
            mail.status = Status.Success
        else:
            mail.status = Status.Failure

        mail.recipient = recipient

        # write to influxdb
        points = [influxdb_client.Point(
            "mail").tag("id", str(mail.id))
                  .tag("sender", str(mail.sender))
                  .tag("status", str(mail.status.value))
                  .time(int(mail.timestamp * 10 ** 6) * 1000)
                  .field("data", mail.json())]
        self.write(points)
        return mail.dict()


if __name__ == "__main__":
    f = APIMailFunction()
    # asyncio.run(f.get_account_data())

    # f.change_account_group_to_recipient(
    #     ["NADI_Admin"], ["admins", "kpc001", "kpc006"],
    #     ["wwilson008@gmail.com", "Daniel@gmail.com"], account_list=account_list, account_info=account_info)
