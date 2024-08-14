from general_operator.function.exception import GeneralOperatorException
from sqlalchemy.exc import OperationalError, DisconnectionError
def create_get_db(db_session):
    def get_db():
        try:
            db = db_session()
            yield db
        except (OperationalError, DisconnectionError) as e:
            raise GeneralOperatorException(status_code=444, detail=f"{e}")
        finally:
            db.close()
    return get_db
