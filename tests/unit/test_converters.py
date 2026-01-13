import pytest
from app.utils.converter import itemTupleToDic, tagTupleToDic, userTupleToDic

def test_itemTupleToDic_normal():
    t = (1, "Sword", 5, 10)
    expected = {"id": 1, "name": "Sword", "sell_in": 5, "quality": 10}
    assert itemTupleToDic(t) == expected

def test_tagTupleToDic_normal():
    t = (10, "Weapon", 1)
    expected = {"id": 10, "name": "Weapon", "item_id": 1}
    assert tagTupleToDic(t) == expected

def test_userTupleToDic_normal():
    t = (100, "Alice", "alice@example.com")
    expected = {"id": 100, "name": "Alice", "email": "alice@example.com"}
    assert userTupleToDic(t) == expected
