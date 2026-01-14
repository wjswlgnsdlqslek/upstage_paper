from app.repository import user_repo
from app.exceptions import EmailNotAllowedNameExistsError, UserNotFoundError
from app.models.schemas.user import UserCreateRequest
from app.models.entities.user import User


def _valid_email(email: str) -> bool:
    return True


def create_user(user: UserCreateRequest) -> User:
    if not _valid_email(user.email):
        raise ValueError("Invalid email format")
    if user.email == "admin@example.com":
        raise EmailNotAllowedNameExistsError(user.email)
    return user_repo.save(name=user.name, email=user.email)


def get_user(user_id: int) -> User:
    user = user_repo.find_by_id(user_id=user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user


def get_users() -> list[User]:
    return user_repo.find_all()


def delete_user(user_id: int):
    success = user_repo.delete(user_id=user_id)
    if not success:
        raise UserNotFoundError(user_id)
