from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    Success = "Success"
    Failure = "Failure"

class Account(BaseModel):
    username: str
    email: str
    name: str


class Recipient(BaseModel):
    group: str
    account: list[Account] = []

class Mail(BaseModel):
    id: int
    sender: str
    subject: str
    message: str
    status: Status = Status.Failure
    recipient: list[Recipient] = []
    timestamp: float

class MailCreate(BaseModel):
    sender: str
    subject: str
    message: str
    groups: list[str]
    accounts: list[str]
    emails: list[str]

