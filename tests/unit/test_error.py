import pytest
from fastapi import HTTPException
from app.domain.errors import item_not_found


def test_item_not_found_raises_http_exception():
    with pytest.raises(HTTPException) as exc:
        item_not_found("abc123")

    err = exc.value

    assert err.status_code == 404

    detail = err.detail
    assert detail["title"] == "Item not found"
    assert detail["status"] == 404
    assert detail["type"] == "https://example.com/problems/item-not-found"
    assert "abc123" in detail["detail"]
