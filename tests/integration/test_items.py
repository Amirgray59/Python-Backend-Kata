import pytest

@pytest.mark.asyncio
async def test_create_item(async_client):
    payload = {"name": "test_item", "sell_in": 5, "quality": 10, "owner_id": 1, "tags": ["tag1","tag2"]}
    response = await async_client.post("/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test_item"
    assert data["owner"]["name"] == "Alice"
    assert "id" in data
    assert data["tags"] == ["tag1","tag2"]

@pytest.mark.asyncio
async def test_get_item(async_client):
    payload = {"name": "item_for_get", "sell_in": 3, "quality": 5, "owner_id": 1, "tags": ["t1"]}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    response = await async_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "item_for_get"
    assert data["owner"]["name"] == "Alice"

@pytest.mark.asyncio
async def test_get_all_items(async_client):
    for i in range(3):
        payload = {"name": f"item{i}", "sell_in": i, "quality": i*10, "owner_id": 1, "tags": []}
        await async_client.post("/items", json=payload)

    response = await async_client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3 

@pytest.mark.asyncio
async def test_update_item(async_client):
    payload = {"name": "old_name", "sell_in": 5, "quality": 5, "owner_id": 1, "tags": ["old"]}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    update_payload = {"name": "new_name", "sell_in": 10, "quality": 15, "tags": ["new1","new2"]}
    response = await async_client.put(f"/items/{item_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "new_name"
    assert data["sell_in"] == 10
    assert data["tags"] == ["new1","new2"]

@pytest.mark.asyncio
async def test_create_item_owner_not_found(async_client):
    payload = {"name": "no_owner", "sell_in": 1, "quality": 1, "owner_id": 999, "tags": []}
    response = await async_client.post("/items", json=payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_item_not_found(async_client):
    response = await async_client.get("/items/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]



@pytest.mark.asyncio
async def test_update_item_not_found(async_client):
    update_payload = {"name": "new_name"}
    response = await async_client.put("/items/99999", json=update_payload)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_item_partial(async_client):
    payload = {"name": "partial", "sell_in": 5, "quality": 5, "owner_id": 1, "tags": ["tag1"]}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    update_payload = {"quality": 99}  
    response = await async_client.put(f"/items/{item_id}", json=update_payload)
    data = response.json()
    assert data["quality"] == 99
    assert data["name"] == "partial"  



@pytest.mark.asyncio
async def test_get_nonexistent_item(async_client):
    response = await async_client.get("/items/9999")
    assert response.status_code == 404
    data = response.json()
    assert "Item with id 9999 not found" in data["detail"]


@pytest.mark.asyncio
async def test_update_item_no_fields(async_client):
    payload = {"name": "up_test", "sell_in": 5, "quality": 5, "owner_id": 1, "tags": ["t1"]}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    update_payload = {"name": None, "sell_in": None, "quality": None, "tags": None}
    response = await async_client.put(f"/items/{item_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "up_test"
    assert data["sell_in"] == 5
    assert data["quality"] == 5
    assert data["tags"] == ["t1"]

@pytest.mark.asyncio
async def test_update_item_mongo_missing_upsert(async_client, monkeypatch):
    payload = {"name": "mongo_missing", "sell_in": 1, "quality": 1, "owner_id": 1, "tags": []}
    create_resp = await async_client.post("/items", json=payload)
    item_id = create_resp.json()["id"]

    from app.api.routes import item
    async def fake_find_one_none(query):
        return None
    item.mongo_db.items_read.find_one = fake_find_one_none

    update_payload = {"name": "updated", "sell_in": 2, "quality": 2, "tags": ["t2"]}
    response = await async_client.put(f"/items/{item_id}", json=update_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item_not_found(async_client, monkeypatch):
    def fake_get_db_none():
        class FakeSession:
            def query(self, model):
                class Query:
                    def filter(self, condition):
                        class Filter:
                            def first(self):
                                return None  
                            def delete(self):
                                return None
                        return Filter()
                return Query()
            def add(self, obj): pass
            def add_all(self, objs): pass
            def commit(self): pass
            def refresh(self, obj): pass
            def delete(self, obj): pass
        return FakeSession()
    monkeypatch.setattr("app.api.routes.item.get_db", fake_get_db_none)

    response = await async_client.delete("/items/9999")
    assert response.status_code == 404
    assert "Item with id 9999 not found" in response.json()["detail"]
