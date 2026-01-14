from fastapi import APIRouter, HTTPException
from app.service import chat_service
from app.models.schemas.chat import ChatCreateRequest, ChatResponse

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatResponse)
async def create_chat_api(chat_create_request: ChatCreateRequest):
    try:
        chat = chat_service.create_chat(chat_create_request)
        return ChatResponse(
            id=chat.id,
            user_id=chat.user_id,
            role=chat.role,
            message=chat.message,
            created_at=str(chat.created_at)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=list[ChatResponse])
async def get_chats_api(user_id: int):
    chats = chat_service.get_recent_conversations(user_id)
    return [
        ChatResponse(
            id=chat.id,
            user_id=chat.user_id,
            role=chat.role,
            message=chat.message,
            created_at=str(chat.created_at)
        ) for chat in chats
    ]
