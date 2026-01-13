import pytest
from fastapi import HTTPException
from app.domain import errors

def test_item_not_found():
    with pytest.raises(HTTPException) as exc:
        errors.item_not_found(42)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Item with id 42 not found"

def test_email_already_exist():
    with pytest.raises(HTTPException) as exc:
        errors.email_already_exist("test@example.com")
    assert exc.value.status_code == 403
    assert exc.value.detail == "Email already exist: test@example.com"

def test_invalid_type():
    with pytest.raises(HTTPException) as exc:
        errors.invalid_type("Invalid data type")
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid data type"

def test_owner_not_found():
    with pytest.raises(HTTPException) as exc:
        errors.owner_not_found(7)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Owner with id 7 not found"
