from datetime import datetime
from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    content: str
    created_at: datetime
