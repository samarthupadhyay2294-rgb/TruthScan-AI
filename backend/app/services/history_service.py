from sqlalchemy.ext.asyncio import AsyncSession

from app.database import crud
from app.schemas.history import HistoryItemResponse, HistoryListResponse


class HistoryService:
    async def list_history(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> HistoryListResponse:
        skip = (page - 1) * page_size
        items = await crud.list_predictions_by_user(db, user_id, skip=skip, limit=page_size)
        total = await crud.count_predictions_by_user(db, user_id)
        return HistoryListResponse(
            items=[HistoryItemResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def delete_history_item(
        self, db: AsyncSession, *, user_id: int, prediction_id: int
    ) -> bool:
        return await crud.delete_prediction(db, prediction_id, user_id)


history_service = HistoryService()
