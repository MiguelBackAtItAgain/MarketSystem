import pytest
from src.models.item import Item

def test_item_initialization():
    item = Item("apple", 5, 1.00, 0.80, True)
    assert item.name == "apple"
    assert item.quantity == 5
    assert item.regular_price == 1.00
    assert item.member_price == 0.80
    assert item.taxable is True