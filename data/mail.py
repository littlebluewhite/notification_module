from app.SQL import models
from schemas import mail

name = "mail"
redis_tables = []
sql_model = models.MailCounter
main_schemas = mail.Mail
create_schemas = mail.MailCreate
update_schemas = None
multiple_update_schemas = None
reload_related_redis_tables = {}