from typing import Any

from fastapi import APIRouter, Query, status

from app.core.dependencies import AdminUser, DbSession
from app.core.exceptions import NotFoundError
from app.database import crud
from app.schemas.auth import MessageResponse
from app.schemas.prediction import PredictionResponse
from app.schemas.user import AdminUserResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[AdminUserResponse])
async def list_users(
    _admin: AdminUser,
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    users = await crud.list_users(db, skip=skip, limit=limit)
    return [AdminUserResponse.model_validate(user) for user in users]


@router.get("/predictions", response_model=list[PredictionResponse])
async def list_all_predictions(
    _admin: AdminUser,
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    predictions = await crud.list_all_predictions(db, skip=skip, limit=limit)
    return [PredictionResponse.model_validate(p) for p in predictions]


@router.get("/analytics")
async def get_analytics(_admin: AdminUser, db: DbSession) -> dict[str, Any]:
    return await crud.get_admin_analytics(db)


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    admin: AdminUser,
    db: DbSession,
):
    if user_id == admin.id:
        raise NotFoundError("Cannot delete your own admin account")
    deleted = await crud.delete_user(db, user_id)
    if not deleted:
        raise NotFoundError("User not found")
    return MessageResponse(message="User deleted successfully")
