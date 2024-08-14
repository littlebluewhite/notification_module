from app.SQL import models
from schemas.API import api_mail

name = "mail"
redis_tables = []
sql_model = models.MailCounter
main_schemas = api_mail.Mail
create_schemas = api_mail.MailCreate
update_schemas = None
multiple_update_schemas = None
reload_related_redis_tables = {}