from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DbSession
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import get_password_hash, verify_password
from app.database import crud
from app.schemas.auth import MessageResponse
from app.schemas.user import (
    PasswordChangeRequest,
    UserProfileResponse,
    UserProfileUpdateRequest,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=UserProfileResponse)
async def get_profile(current_user: CurrentUser):
    return UserProfileResponse.model_validate(current_user)


@router.put("", response_model=UserProfileResponse)
async def update_profile(
    payload: UserProfileUpdateRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    if payload.username and payload.username != current_user.username:
        existing = await crud.get_user_by_username(db, payload.username)
        if existing:
            raise ConflictError("Username already taken")

    updated = await crud.update_user(
        db,
        current_user,
        full_name=payload.full_name,
        username=payload.username,
    )
    return UserProfileResponse.model_validate(updated)


@router.put("/password", response_model=MessageResponse)
async def change_password(
    payload: PasswordChangeRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise UnauthorizedError("Current password is incorrect")

    await crud.update_user(
        db,
        current_user,
        hashed_password=get_password_hash(payload.new_password),
    )
    return MessageResponse(message="Password updated successfully")


@router.delete("", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_profile(current_user: CurrentUser, db: DbSession):
    await crud.delete_user(db, current_user.id)
    return MessageResponse(message="Account deleted successfully")
