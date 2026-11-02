import pytest

from config.config import api_config
from tests.api.clients.users_client import UsersClient
from tests.api.builders.user_builder import UserBuilder


@pytest.fixture(scope="session")
def users_client():
    if not api_config.API_KEY:
        pytest.skip("REQRES_API_KEY is not set")
    client = UsersClient(api_config.BASE_URL, api_config.API_KEY)
    yield client
    client.close()


@pytest.fixture
def created_user(users_client):
    payload = UserBuilder().build()
    response = users_client.create_user(payload=payload)
    assert response.status_code == 201, response.text
    user = response.json()
    yield user
    users_client.delete_user(user_id=user["id"])
