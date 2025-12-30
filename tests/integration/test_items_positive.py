def test_create_item_success(client):
    response = client.post(
        "/items",
        json={"name": "Foo", "sell_in": 10, "quality": 20},
    )

    assert response.status_code == 201
    body = response.json()

    assert "id" in body
    assert body["name"] == "Foo"
    assert body["sell_in"] == 10
    assert body["quality"] == 20


def test_get_item_success(client):
    create = client.post(
        "/items",
        json={"name": "Bar", "sell_in": 5, "quality": 7},
    )
    item_id = create.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Bar"


def test_update_item_success(client):
    create = client.post(
        "/items",
        json={"name": "Baz", "sell_in": 3, "quality": 6},
    )
    item_id = create.json()["id"]

    response = client.patch(
        f"/items/{item_id}",
        json={"quality": 9},
    )

    assert response.status_code == 200
    assert response.json()["quality"] == 9


def test_delete_item_success(client):
    create = client.post(
        "/items",
        json={"name": "Qux", "sell_in": 1, "quality": 1},
    )
    item_id = create.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
