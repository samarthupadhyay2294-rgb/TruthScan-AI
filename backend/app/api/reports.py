from fastapi import APIRouter, Query, status

from app.core.dependencies import CurrentUser, DbSession
from app.schemas.report import ReportListResponse, ReportResponse
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("", response_model=ReportListResponse)
async def list_reports(
    current_user: CurrentUser,
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    return await report_service.list_reports(
        db, user_id=current_user.id, skip=skip, limit=limit
    )


@router.post("/{prediction_id}", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    prediction_id: int,
    current_user: CurrentUser,
    db: DbSession,
):
    return await report_service.create_report(
        db, user=current_user, prediction_id=prediction_id
    )
