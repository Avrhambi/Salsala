"""
SQLAlchemy async ORM table definitions for core Salsala tables.
All primary keys are UUIDs. Timestamps use server-side defaults.
"""
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)

    lists: Mapped[list["ShoppingListORM"]] = relationship(
        "ShoppingListORM", secondary="list_members", back_populates="users"
    )


class ItemORM(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name_hebrew: Mapped[str] = mapped_column(String(255), nullable=False)
    default_quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class ShoppingListORM(Base):
    __tablename__ = "shopping_lists"

    list_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="My List")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sync_timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    users: Mapped[list[UserORM]] = relationship(
        "UserORM", secondary="list_members", back_populates="lists"
    )


class ListMemberORM(Base):
    """Association table — many-to-many between lists and users."""

    __tablename__ = "list_members"

    list_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("shopping_lists.list_id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True
    )


class ListItemORM(Base):
    """Association table — items belonging to a shopping list."""

    __tablename__ = "list_items"

    list_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("shopping_lists.list_id"), primary_key=True
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_bought: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
