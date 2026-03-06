from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.controllers.transaction import handle_purchase
from server.db.client import get_db_session
from server.models.transaction import Transaction

router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.post("/purchase")
async def log_purchase(
    transaction: Transaction,
    db: AsyncSession = Depends(get_db_session),
):
    return await handle_purchase(transaction, db)
