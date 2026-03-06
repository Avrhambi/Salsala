from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.transaction import Transaction
from server.services import transaction as transaction_service
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def handle_purchase(
    transaction: Transaction,
    db: AsyncSession,
):
    """
    Record a 'Mark as Bought' event.
    Pydantic enforces price > 0 and quantity > 0 at deserialization —
    no structurally invalid Transaction can reach this controller.
    """
    try:
        logged = await transaction_service.create_transaction_log(transaction, db)
        return logged
    except NotImplementedError as exc:
        _logger.error("Transaction service not implemented: %s", exc)
        raise HTTPException(
            status_code=501, detail="Transaction service not yet available."
        )
    except ValueError as exc:
        _logger.warning("Transaction validation error: %s", exc)
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        _logger.error("Unexpected purchase error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
