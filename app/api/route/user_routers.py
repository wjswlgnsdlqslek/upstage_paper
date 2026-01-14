from fastapi import APIRouter, HTTPException
from app.service import user_service
from app.models.schemas.user import UserCreateRequest, UserResponse
from app.exceptions import UserNotFoundError, EmailNotAllowedNameExistsError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user_api(user_create_request: UserCreateRequest):
    try:
        user = user_service.create_user(user_create_request)
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=str(user.created_at)
        )
    except EmailNotAllowedNameExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_api(user_id: int):
    try:
        user = user_service.get_user(user_id)
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=str(user.created_at)
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[UserResponse])
async def get_users_api():
    users = user_service.get_users()
    return [
        UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=str(user.created_at)
        ) for user in users
    ]


@router.delete("/{user_id}")
async def delete_user_api(user_id: int):
    try:
        user_service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "User deleted"}
