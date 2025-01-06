from app.SQL import models
from schemas import notify

name = "notify"
redis_tables = []
sql_model = models.NotifyCounter
main_schemas = notify.Notify
create_schemas = notify.NotifyCreate
update_schemas = None
multiple_update_schemas = None
reload_related_redis_tables = {}