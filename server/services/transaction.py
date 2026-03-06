from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from server.models.transaction import Transaction
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def create_transaction_log(
    transaction: Transaction, db: AsyncSession
) -> Transaction:
    """
    Persist a validated transaction to the purchase history log.
    The Transaction model enforces price > 0 at the Pydantic layer,
    so this service receives only clean data.
    """
    if not transaction:
        raise ValueError("transaction must not be None.")

    try:
        persisted = await _write_transaction(transaction, db)
        _logger.info(
            "Transaction %s logged: item=%s store='%s' price=%.2f.",
            persisted.transaction_id,
            persisted.item_id,
            persisted.store_name,
            persisted.price,
        )
        return persisted
    except Exception as exc:
        _logger.error(
            "Failed to log transaction %s: %s", transaction.transaction_id, exc
        )
        raise


async def get_transaction_history(item_id: UUID, db: AsyncSession) -> list[Transaction]:
    """Retrieve all purchase transactions for a given item."""
    if not item_id:
        raise ValueError("item_id must not be None.")

    try:
        _logger.debug("Fetching transaction history for item %s.", item_id)
        # Placeholder — replace with: await db.execute(select(TransactionORM)...)
        return []
    except Exception as exc:
        _logger.error("Failed to fetch history for item %s: %s", item_id, exc)
        raise


async def _write_transaction(transaction: Transaction, db: AsyncSession) -> Transaction:
    """Insert the transaction record into the database."""
    _logger.debug("Writing transaction %s.", transaction.transaction_id)
    # Placeholder — replace with: db.add(orm_obj); await db.commit()
    raise NotImplementedError("Database layer not yet connected.")
