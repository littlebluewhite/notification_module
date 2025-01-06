from enum import Enum
from pydantic import BaseModel, Field


class Status(str, Enum):
    Success = "Success"
    Failure = "Failure"

class Account(BaseModel):
    username: str
    email: str
    name: str


class Recipient(BaseModel):
    group: str
    account: list[Account] = Field(default_factory=list)


class Mail(BaseModel):
    id: int
    sender: str
    subject: str
    message: str
    status: Status = Status.Failure
    recipient: list[Recipient] = Field(default_factory=list)

    timestamp: float

class MailCreate(BaseModel):
    sender: str
    subject: str
    message: str
    groups: list[str]
    accounts: list[str]
    emails: list[str]
