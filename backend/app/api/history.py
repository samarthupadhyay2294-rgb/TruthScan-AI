from fastapi import APIRouter, Query, status

from app.core.dependencies import CurrentUser, DbSession
from app.core.exceptions import NotFoundError
from app.schemas.auth import MessageResponse
from app.schemas.history import HistoryListResponse
from app.services.history_service import history_service

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=HistoryListResponse)
async def get_history(
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return await history_service.list_history(
        db, user_id=current_user.id, page=page, page_size=page_size
    )


@router.delete("/{prediction_id}", response_model=MessageResponse)
async def delete_history_item(
    prediction_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    deleted = await history_service.delete_history_item(
        db, user_id=current_user.id, prediction_id=prediction_id
    )
    if not deleted:
        raise NotFoundError("Prediction not found")
    return MessageResponse(message="Prediction deleted successfully")
