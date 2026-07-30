from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.database.base import Base
from app.database.database import engine
from app.middleware.cors import setup_cors
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limit import setup_rate_limiting
from app.ml.predictor import predictor

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)

    try:
        predictor.load()
        logger.info("ML model loaded successfully")
    except FileNotFoundError as exc:
        logger.warning("ML models not loaded at startup: %s", exc)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="TruthLens AI — Fake news detection API powered by LinearSVC + TF-IDF",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    register_exception_handlers(application)
    setup_cors(application)
    setup_rate_limiting(application)
    application.add_middleware(RequestLoggingMiddleware)
    application.include_router(api_router)

    @application.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "model_loaded": predictor.is_loaded,
        }

    return application


app = create_app()
