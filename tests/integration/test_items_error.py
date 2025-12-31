def test_get_item_not_found(client):
    response = client.get("/items/non-existent-id")

    assert response.status_code == 404
    body = response.json()

    assert body["detail"]["title"] == "Item not found"
    assert body["detail"]["status"] == 404


def test_delete_item_not_found(client):
    response = client.delete("/items/non-existent-id")
    assert response.status_code == 404


def test_update_item_not_found(client):
    response = client.patch(
        "/items/non-existent-id",
        json={"quality": 10},
    )
    assert response.status_code == 404


def test_create_item_invalid_quality(client):
    response = client.post(
        "/items",
        json={"name": "Bad", "sell_in": 1, "quality": None},
    )
    assert response.status_code == 422
