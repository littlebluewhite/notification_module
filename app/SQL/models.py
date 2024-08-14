from general_operator.app.SQL.database import Base
from sqlalchemy import Integer, Column, String, DateTime
from datetime import datetime


class MailCounter(Base):
    __tablename__ = "mail_counter"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)

class LineCounter(Base):
    __tablename__ = "line_counter"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)