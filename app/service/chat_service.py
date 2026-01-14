from app.repository import chat_repo
from app.models.schemas.chat import ChatCreateRequest
from app.models.entities.chat import Chat, Role


def create_chat(chat: ChatCreateRequest) -> Chat:
    # In a real application, you would have some business logic here.
    # For example, you might want to check if the user exists.
    # You might also want to do some processing on the message.
    # For now, we will just save the chat.
    # We will assume the user message is saved first, then the assistant message.
    chat_repo.save_chat_transaction(chat.user_id, chat.message, "I am a bot.")
    # This is not ideal, as we are not returning the created chat.
    # We will just return the user message for now.
    return chat_repo.add_conversation(chat.user_id, Role.USER, chat.message)


def get_recent_conversations(user_id: int, limit: int = 20) -> list[Chat]:
    return chat_repo.get_recent_conversations(user_id, limit)


def get_chat(chat_id: int) -> Chat:
    chat = chat_repo.find_by_id(chat_id)
    if not chat:
        raise ValueError(f"Chat with id {chat_id} not found")
    return chat
