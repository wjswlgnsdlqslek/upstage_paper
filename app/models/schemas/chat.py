from pydantic import BaseModel
from app.models.entities.chat import Role


class ChatCreateRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    id: int
    user_id: int
    role: Role
    message: str
    created_at: str
