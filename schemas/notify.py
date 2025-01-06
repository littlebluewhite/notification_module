from pydantic import BaseModel, Field


class Account(BaseModel):
    username: str
    email: str
    name: str


class Recipient(BaseModel):
    group: str
    account: list[Account] = Field(default_factory=list)


class Notify(BaseModel):
    id: int
    sender: str
    subject: str
    message: str
    is_email: bool = False
    is_message: bool = False
    is_line: bool = False
    email_result: dict = Field(default_factory=dict)
    message_result: dict = Field(default_factory=dict)
    line_result: dict = Field(default_factory=dict)
    recipient: list[Recipient] = Field(default_factory=list)
    timestamp: float


class NotifyCreate(BaseModel):
    sender: str
    subject: str
    message: str
    is_email: bool = False
    is_message: bool = False
    is_line: bool = False
    groups: list[str]
    accounts: list[str]
    emails: list[str]
