import uuid
from datetime import datetime, timezone
from typing import List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.orm_models import ShoppingListORM, ListMemberORM, UserORM, ItemORM, ListItemORM
from server.models.item import Item
from server.models.list import ShoppingList
from server.utils.logger import get_logger

_logger = get_logger(__name__)


async def _build_list(row: ShoppingListORM, list_id: UUID, db: AsyncSession) -> ShoppingList:
    member_ids_result = await db.execute(
        select(ListMemberORM.user_id).where(ListMemberORM.list_id == list_id)
    )
    member_ids = [r[0] for r in member_ids_result.all()]

    items_result = await db.execute(
        select(ListItemORM, ItemORM)
        .join(ItemORM, ListItemORM.item_id == ItemORM.id)
        .where(ListItemORM.list_id == list_id)
    )
    items = [
        Item(
            id=item_orm.id,
            name_hebrew=item_orm.name_hebrew,
            default_quantity=li_orm.quantity,
            is_bought=li_orm.is_bought,
        )
        for li_orm, item_orm in items_result.all()
    ]

    return ShoppingList(
        list_id=row.list_id,
        name=row.name,
        users=member_ids or [list_id],
        items=items,
        is_completed=row.is_completed,
        completed_at=row.completed_at,
    )


async def create_list(user_ids: List[UUID], name: str, db: AsyncSession) -> ShoppingList:
    if not user_ids:
        raise ValueError("A list must have at least one user.")
    new_list = ShoppingListORM(name=name)
    db.add(new_list)
    await db.flush()
    for uid in user_ids:
        if not await db.get(UserORM, uid):
            db.add(UserORM(user_id=uid, display_name="Anonymous"))
            await db.flush()
        db.add(ListMemberORM(list_id=new_list.list_id, user_id=uid))
    await db.commit()
    await db.refresh(new_list)
    _logger.info("Created list %s.", new_list.list_id)
    return await _build_list(new_list, new_list.list_id, db)


async def get_list_by_id(list_id: UUID, db: AsyncSession) -> ShoppingList:
    row = await db.get(ShoppingListORM, list_id)
    if row is None:
        raise ValueError(f"List {list_id} not found.")
    return await _build_list(row, list_id, db)


async def add_item_to_list(list_id: UUID, item_id: str, quantity: int, db: AsyncSession) -> ShoppingList:
    if await db.get(ShoppingListORM, list_id) is None:
        raise ValueError(f"List {list_id} not found.")
    item_orm = None
    try:
        item_orm = await db.get(ItemORM, UUID(item_id))
    except ValueError:
        pass
    if item_orm is None:
        item_orm = ItemORM(name_hebrew=item_id, default_quantity=quantity)
        db.add(item_orm)
        await db.flush()
    existing = await db.get(ListItemORM, (list_id, item_orm.id))
    if existing:
        existing.quantity = quantity
    else:
        db.add(ListItemORM(list_id=list_id, item_id=item_orm.id, quantity=quantity))
    await db.commit()
    _logger.info("Added item %s to list %s.", item_orm.id, list_id)
    return await get_list_by_id(list_id, db)


async def remove_item_from_list(list_id: UUID, item_id: UUID, db: AsyncSession) -> ShoppingList:
    if await db.get(ShoppingListORM, list_id) is None:
        raise ValueError(f"List {list_id} not found.")
    await db.execute(
        delete(ListItemORM).where(ListItemORM.list_id == list_id, ListItemORM.item_id == item_id)
    )
    await db.commit()
    return await get_list_by_id(list_id, db)


async def rename_list(list_id: UUID, name: str, db: AsyncSession) -> ShoppingList:
    row = await db.get(ShoppingListORM, list_id)
    if row is None:
        raise ValueError(f"List {list_id} not found.")
    row.name = name
    await db.commit()
    return await get_list_by_id(list_id, db)


async def delete_list(list_id: UUID, db: AsyncSession) -> None:
    row = await db.get(ShoppingListORM, list_id)
    if row is None:
        raise ValueError(f"List {list_id} not found.")
    await db.execute(delete(ListItemORM).where(ListItemORM.list_id == list_id))
    await db.execute(delete(ListMemberORM).where(ListMemberORM.list_id == list_id))
    await db.delete(row)
    await db.commit()
    _logger.info("Deleted list %s.", list_id)


async def mark_item_bought(list_id: UUID, item_id: UUID, db: AsyncSession) -> ShoppingList:
    existing = await db.get(ListItemORM, (list_id, item_id))
    if existing is None:
        raise ValueError(f"Item {item_id} not in list {list_id}.")
    existing.is_bought = True
    await db.commit()
    await _check_and_archive(list_id, db)
    return await get_list_by_id(list_id, db)


async def _check_and_archive(list_id: UUID, db: AsyncSession) -> None:
    result = await db.execute(select(ListItemORM).where(ListItemORM.list_id == list_id))
    items = result.scalars().all()
    if items and all(i.is_bought for i in items):
        row = await db.get(ShoppingListORM, list_id)
        if row and not row.is_completed:
            row.is_completed = True
            row.completed_at = datetime.now(timezone.utc)
            await db.commit()
            _logger.info("List %s archived.", list_id)


async def get_history(user_id: UUID, db: AsyncSession) -> List[ShoppingList]:
    ids_result = await db.execute(
        select(ListMemberORM.list_id).where(ListMemberORM.user_id == user_id)
    )
    list_ids = [r[0] for r in ids_result.all()]
    if not list_ids:
        return []
    rows_result = await db.execute(
        select(ShoppingListORM).where(
            ShoppingListORM.list_id.in_(list_ids),
            ShoppingListORM.is_completed == True,
        )
    )
    rows = rows_result.scalars().all()
    return [await _build_list(row, row.list_id, db) for row in rows]
