from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from server.config.settings import get_settings
from server.utils.logger import get_logger

_logger = get_logger(__name__)

_engine = None
_async_session_factory = None


def _get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.database_url,
            echo=False,
            pool_size=10,
            max_overflow=20,
        )
        _logger.info("Database engine initialized.")
    return _engine


def _get_session_factory():
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = sessionmaker(
            _get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a managed async database session."""
    session_factory = _get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            _logger.error("Database session error, rolling back: %s", exc)
            raise
        finally:
            await session.close()
