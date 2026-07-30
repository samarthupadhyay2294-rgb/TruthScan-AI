from fastapi import APIRouter, File, Request, UploadFile, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.dependencies import DbSession, OptionalUser
from app.schemas.prediction import PredictRequest, PredictResultResponse
from app.services.prediction_service import prediction_service
from app.utils.file_handler import extract_text_from_upload, validate_upload_file

router = APIRouter(prefix="/predict", tags=["Prediction"])
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=PredictResultResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PREDICT)
async def predict_text(
    request: Request,
    payload: PredictRequest,
    current_user: OptionalUser,
    db: DbSession,
):
    return await prediction_service.predict_text(
        db, user=current_user, text=payload.text, source="manual"
    )


upload_router = APIRouter(tags=["Upload"])


@upload_router.post("/upload", response_model=PredictResultResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PREDICT)
async def upload_and_predict(
    request: Request,
    current_user: OptionalUser,
    db: DbSession,
    file: UploadFile = File(...),
):
    validate_upload_file(file)
    text = await extract_text_from_upload(file)
    return await prediction_service.predict_text(
        db,
        user=current_user,
        text=text,
        source="upload",
        filename=file.filename,
    )
