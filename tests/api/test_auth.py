from config.config import api_config
from tests.api.clients.base_client import BaseClient


def test_login_with_valid_credentials_returns_a_token(users_client):
    credentials = {"email": "eve.holt@reqres.in", "password": "cityslicka"}

    response = users_client.post("/login", json=credentials)

    assert response.status_code == 200
    assert response.json()["token"]


def test_login_without_password_returns_400_and_names_the_field(users_client):
    credentials = {"email": "eve.holt@reqres.in"}

    response = users_client.post("/login", json=credentials)

    assert response.status_code == 400
    assert "password" in response.json()["error"].lower()


def test_register_with_valid_credentials_returns_id_and_token(users_client):
    credentials = {"email": "eve.holt@reqres.in", "password": "pistol"}

    response = users_client.post("/register", json=credentials)

    body = response.json()
    assert response.status_code == 200
    assert "id" in body
    assert body["token"]


# def test_request_without_api_key_is_rejected_with_401():
#     client = BaseClient(api_config.BASE_URL)
#     try:
#         response = client.get("/users/2")
#     finally:
#         client.close()

#     assert response.status_code == 401
