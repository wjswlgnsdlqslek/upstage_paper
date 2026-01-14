from pydantic import BaseModel


class TodoCreateRequest(BaseModel):
    content: str


class TodoResponse(BaseModel):
    id: int
    content: str
    created_at: str
