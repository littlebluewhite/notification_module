from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    Success = "Success"
    Failure = "Failure"


class Mail(BaseModel):
    id: int
    sender: str
    subject: str
    message: str
    status: Status = Status.Failure
    recipient: list = []
    timestamp: float


class MailCreate(BaseModel):
    sender: str
    subject: str
    message: str
    groups: list[str]
    accounts: list[str]
    emails: list[str]

