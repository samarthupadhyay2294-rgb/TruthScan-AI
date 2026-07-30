from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.database import engine

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
