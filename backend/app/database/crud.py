from datetime import datetime, timezone
from typing import Any, Optional, Sequence

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import PasswordResetToken, Prediction, Report, User


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    *,
    email: str,
    username: str,
    hashed_password: str,
    full_name: Optional[str] = None,
) -> User:
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, **fields: Any) -> User:
    for key, value in fields.items():
        if value is not None and hasattr(user, key):
            setattr(user, key, value)
    await db.flush()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(delete(User).where(User.id == user_id))
    return result.rowcount > 0


async def list_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[User]:
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_prediction(
    db: AsyncSession,
    *,
    user_id: Optional[int] = None,
    text: str,
    cleaned_text: str,
    label: int,
    label_name: str,
    confidence: float,
    source: str = "manual",
    filename: Optional[str] = None,
    analysis: Optional[dict[str, Any]] = None,
) -> Prediction:
    prediction = Prediction(
        user_id=user_id,
        text=text,
        cleaned_text=cleaned_text,
        label=label,
        label_name=label_name,
        confidence=confidence,
        source=source,
        filename=filename,
        analysis=analysis,
    )
    db.add(prediction)
    await db.flush()
    await db.refresh(prediction)
    return prediction


async def get_prediction_by_id(
    db: AsyncSession, prediction_id: int, user_id: Optional[int] = None
) -> Optional[Prediction]:
    query = select(Prediction).where(Prediction.id == prediction_id)
    if user_id is not None:
        query = query.where(Prediction.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_predictions_by_user(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
) -> Sequence[Prediction]:
    result = await db.execute(
        select(Prediction)
        .where(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def delete_prediction(db: AsyncSession, prediction_id: int, user_id: int) -> bool:
    result = await db.execute(
        delete(Prediction).where(
            Prediction.id == prediction_id, Prediction.user_id == user_id
        )
    )
    return result.rowcount > 0


async def count_predictions_by_user(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(
        select(func.count()).select_from(Prediction).where(Prediction.user_id == user_id)
    )
    return result.scalar_one()


async def get_user_prediction_stats(db: AsyncSession, user_id: int) -> dict[str, Any]:
    total = await count_predictions_by_user(db, user_id)
    fake_result = await db.execute(
        select(func.count())
        .select_from(Prediction)
        .where(Prediction.user_id == user_id, Prediction.label == 0)
    )
    real_result = await db.execute(
        select(func.count())
        .select_from(Prediction)
        .where(Prediction.user_id == user_id, Prediction.label == 1)
    )
    avg_confidence_result = await db.execute(
        select(func.avg(Prediction.confidence)).where(Prediction.user_id == user_id)
    )
    return {
        "total": total,
        "fake_count": fake_result.scalar_one(),
        "real_count": real_result.scalar_one(),
        "avg_confidence": float(avg_confidence_result.scalar_one() or 0.0),
    }


async def list_all_predictions(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Prediction]:
    result = await db.execute(
        select(Prediction).order_by(Prediction.created_at.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_admin_analytics(db: AsyncSession) -> dict[str, Any]:
    user_count = await db.execute(select(func.count()).select_from(User))
    prediction_count = await db.execute(select(func.count()).select_from(Prediction))
    fake_count = await db.execute(
        select(func.count()).select_from(Prediction).where(Prediction.label == 0)
    )
    real_count = await db.execute(
        select(func.count()).select_from(Prediction).where(Prediction.label == 1)
    )
    report_count = await db.execute(select(func.count()).select_from(Report))
    return {
        "total_users": user_count.scalar_one(),
        "total_predictions": prediction_count.scalar_one(),
        "fake_predictions": fake_count.scalar_one(),
        "real_predictions": real_count.scalar_one(),
        "total_reports": report_count.scalar_one(),
    }


async def create_report(
    db: AsyncSession,
    *,
    user_id: int,
    prediction_id: int,
    title: str,
    summary: Optional[str],
    content: dict[str, Any],
    pdf_path: Optional[str] = None,
) -> Report:
    report = Report(
        user_id=user_id,
        prediction_id=prediction_id,
        title=title,
        summary=summary,
        content=content,
        pdf_path=pdf_path,
    )
    db.add(report)
    await db.flush()
    await db.refresh(report)
    return report


async def get_report_by_prediction_id(
    db: AsyncSession, prediction_id: int, user_id: Optional[int] = None
) -> Optional[Report]:
    query = select(Report).where(Report.prediction_id == prediction_id)
    if user_id is not None:
        query = query.where(Report.user_id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_reports_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 50
) -> Sequence[Report]:
    result = await db.execute(
        select(Report)
        .where(Report.user_id == user_id)
        .order_by(Report.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_password_reset_token(
    db: AsyncSession, user_id: int, token: str, expires_at: datetime
) -> PasswordResetToken:
    reset_token = PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )
    db.add(reset_token)
    await db.flush()
    await db.refresh(reset_token)
    return reset_token


async def get_valid_password_reset_token(
    db: AsyncSession, token: str
) -> Optional[PasswordResetToken]:
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token,
            PasswordResetToken.used.is_(False),
            PasswordResetToken.expires_at > datetime.now(timezone.utc),
        )
    )
    return result.scalar_one_or_none()


async def mark_password_reset_token_used(db: AsyncSession, token_id: int) -> None:
    await db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.id == token_id)
        .values(used=True)
    )


async def invalidate_user_password_reset_tokens(db: AsyncSession, user_id: int) -> None:
    await db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.user_id == user_id, PasswordResetToken.used.is_(False))
        .values(used=True)
    )
