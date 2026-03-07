"""
Unit tests for MVP Pydantic models — Item and ShoppingList.
No DB or HTTP dependencies required.
"""
import pytest
from uuid import uuid4

from server.models.item import Item
from server.models.list import ShoppingList


# ── Item ──────────────────────────────────────────────────────────────────────

def test_item_valid():
    item = Item(id=uuid4(), name_hebrew="חלב", default_quantity=2, is_bought=False)
    assert item.name_hebrew == "חלב"
    assert item.default_quantity == 2
    assert item.is_bought is False


def test_item_strips_whitespace():
    item = Item(id=uuid4(), name_hebrew="  לחם  ", default_quantity=1, is_bought=False)
    assert item.name_hebrew == "לחם"


def test_item_raises_for_empty_name():
    with pytest.raises(Exception):
        Item(id=uuid4(), name_hebrew="", default_quantity=1, is_bought=False)


def test_item_raises_for_whitespace_name():
    with pytest.raises(Exception):
        Item(id=uuid4(), name_hebrew="   ", default_quantity=1, is_bought=False)


def test_item_raises_for_negative_quantity():
    with pytest.raises(Exception):
        Item(id=uuid4(), name_hebrew="חלב", default_quantity=-1, is_bought=False)


def test_item_allows_zero_quantity():
    item = Item(id=uuid4(), name_hebrew="חלב", default_quantity=0, is_bought=False)
    assert item.default_quantity == 0


def test_item_is_bought_defaults_false():
    item = Item(id=uuid4(), name_hebrew="ביצים", default_quantity=1)
    assert item.is_bought is False


# ── ShoppingList ──────────────────────────────────────────────────────────────

def test_shopping_list_valid():
    uid = uuid4()
    sl = ShoppingList(
        list_id=uuid4(), name="קניות שבועיות",
        users=[uid], items=[], is_completed=False, completed_at=None,
    )
    assert sl.name == "קניות שבועיות"
    assert len(sl.users) == 1
    assert sl.is_completed is False


def test_shopping_list_raises_for_empty_users():
    with pytest.raises(Exception):
        ShoppingList(
            list_id=uuid4(), name="Test",
            users=[], items=[], is_completed=False, completed_at=None,
        )


def test_shopping_list_is_completed_defaults_false():
    sl = ShoppingList(
        list_id=uuid4(), name="Test",
        users=[uuid4()], items=[],
    )
    assert sl.is_completed is False
    assert sl.completed_at is None


def test_shopping_list_accepts_multiple_users():
    users = [uuid4(), uuid4(), uuid4()]
    sl = ShoppingList(
        list_id=uuid4(), name="משפחתי",
        users=users, items=[], is_completed=False, completed_at=None,
    )
    assert len(sl.users) == 3


def test_shopping_list_with_items():
    item = Item(id=uuid4(), name_hebrew="חלב", default_quantity=1, is_bought=False)
    sl = ShoppingList(
        list_id=uuid4(), name="Test",
        users=[uuid4()], items=[item], is_completed=False, completed_at=None,
    )
    assert len(sl.items) == 1
    assert sl.items[0].name_hebrew == "חלב"
