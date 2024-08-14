from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    Success = "Success"
    Failure = "Failure"


class Line(BaseModel):
    id: int
    message: str
    status: Status
    timestamp: float


class LineCreate(BaseModel):
    message: str
    group: list[str]
    account: list[str]

