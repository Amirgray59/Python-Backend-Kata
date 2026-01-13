import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.db.mongo import session


def test_get_mongo_client_creates_client_once():
    session._client = None

    with patch("app.db.mongo.session.AsyncIOMotorClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance

        client1 = session.get_mongo_client()
        client2 = session.get_mongo_client()

        assert client1 is client2
        mock_client.assert_called_once_with(session.MONGO_URL)


def test_get_mongo_db_returns_db():
    fake_client = MagicMock()
    fake_client.__getitem__.return_value = "my_db"
    with patch("app.db.mongo.session.get_mongo_client", return_value=fake_client):
        db = session.get_mongo_db()
        assert db == "my_db"
        fake_client.__getitem__.assert_called_with("items")


@pytest.mark.asyncio
async def test_get_mongo_returns_app_state_mock():
    class FakeRequest:
        class AppState:
            mongo = "my_mongo"
        app = AppState()

    fake_request = FakeRequest()
