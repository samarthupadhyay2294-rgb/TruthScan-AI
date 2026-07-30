from pathlib import Path
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.report_generator import build_report_content, generate_pdf_report
from app.core.config import settings
from app.core.exceptions import ConflictError, NotFoundError
from app.database import crud
from app.database.models import User
from app.schemas.report import ReportListResponse, ReportResponse


class ReportService:
    def __init__(self) -> None:
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    async def create_report(
        self, db: AsyncSession, *, user: User, prediction_id: int
    ) -> ReportResponse:
        existing = await crud.get_report_by_prediction_id(db, prediction_id, user.id)
        if existing:
            raise ConflictError("Report already exists for this prediction")

        prediction = await crud.get_prediction_by_id(db, prediction_id, user.id)
        if not prediction:
            raise NotFoundError("Prediction not found")

        analysis = prediction.analysis or {}
        title = f"Analysis Report #{prediction.id}"
        content = build_report_content(
            text=prediction.text,
            prediction={
                "label": prediction.label,
                "label_name": prediction.label_name,
                "confidence": prediction.confidence,
                "source": prediction.source,
            },
            analysis=analysis,
        )

        pdf_filename = f"report_{prediction.id}_{uuid4().hex[:8]}.pdf"
        pdf_path = str(self.reports_dir / pdf_filename)
        generate_pdf_report(
            pdf_path,
            title=title,
            text=prediction.text,
            prediction={
                "label_name": prediction.label_name,
                "confidence": prediction.confidence,
                "source": prediction.source,
            },
            analysis=analysis,
        )

        report = await crud.create_report(
            db,
            user_id=user.id,
            prediction_id=prediction_id,
            title=title,
            summary=analysis.get("ai", {}).get("summary"),
            content=content,
            pdf_path=pdf_path,
        )
        return ReportResponse.model_validate(report)

    async def list_reports(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 50
    ) -> ReportListResponse:
        items = await crud.list_reports_by_user(db, user_id, skip=skip, limit=limit)
        return ReportListResponse(
            items=[ReportResponse.model_validate(item) for item in items],
            total=len(items),
        )


report_service = ReportService()
