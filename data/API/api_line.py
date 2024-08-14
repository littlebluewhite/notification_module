from app.SQL import models
from schemas.API import api_line

name = "line"
redis_tables = []
sql_model = models.LineCounter
main_schemas = api_line.Line
create_schemas = api_line.LineCreate
update_schemas = None
multiple_update_schemas = None
reload_related_redis_tables = {}