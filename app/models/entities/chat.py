from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Chat:
    id: int
    user_id: int
    role: Role
    message: str
    created_at: datetime
