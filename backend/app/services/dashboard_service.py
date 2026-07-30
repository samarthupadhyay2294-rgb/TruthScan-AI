from collections import defaultdict
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import crud
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardStatsResponse,
    RecentPredictionItem,
)


class DashboardService:
    async def get_dashboard(self, db: AsyncSession, *, user_id: int) -> DashboardResponse:
        stats_raw = await crud.get_user_prediction_stats(db, user_id)
        total = stats_raw["total"]
        fake_count = stats_raw["fake_count"]
        real_count = stats_raw["real_count"]

        fake_pct = round((fake_count / total * 100) if total else 0.0, 2)
        real_pct = round((real_count / total * 100) if total else 0.0, 2)

        stats = DashboardStatsResponse(
            total_predictions=total,
            fake_count=fake_count,
            real_count=real_count,
            avg_confidence=round(stats_raw["avg_confidence"], 4),
            fake_percentage=fake_pct,
            real_percentage=real_pct,
        )

        recent = await crud.list_predictions_by_user(db, user_id, skip=0, limit=10)
        recent_items = [RecentPredictionItem.model_validate(p) for p in recent]

        all_recent = await crud.list_predictions_by_user(db, user_id, skip=0, limit=100)
        trend_map: dict[str, dict[str, int]] = defaultdict(
            lambda: {"fake": 0, "real": 0, "total": 0}
        )
        for pred in all_recent:
            day_key = pred.created_at.date().isoformat()
            trend_map[day_key]["total"] += 1
            if pred.label == 0:
                trend_map[day_key]["fake"] += 1
            else:
                trend_map[day_key]["real"] += 1

        trend = [
            {"date": date, **counts}
            for date, counts in sorted(trend_map.items(), reverse=True)[:14]
        ]
        trend.reverse()

        return DashboardResponse(
            stats=stats,
            recent_predictions=recent_items,
            trend=trend,
        )


dashboard_service = DashboardService()
