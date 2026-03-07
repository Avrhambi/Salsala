from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.db.orm_models import UserORM
from server.models.user import User
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def create_user(display_name: str, db: AsyncSession) -> User:
    if not display_name or not display_name.strip():
        raise ValueError("display_name must not be empty.")

    orm_user = UserORM(display_name=display_name.strip())
    db.add(orm_user)
    await db.commit()
    await db.refresh(orm_user)
    _logger.info("Created user %s (%s).", orm_user.user_id, orm_user.display_name)

    return User(user_id=orm_user.user_id, display_name=orm_user.display_name)
