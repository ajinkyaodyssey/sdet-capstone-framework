from tests.api.builders.user_builder import UserBuilder


def test_get_user_returns_that_user(users_client):
    response = users_client.get_user(user_id=2)

    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2


def test_get_unknown_user_returns_404(users_client):
    response = users_client.get_user(user_id=23)

    assert response.status_code == 404


def test_create_user_echoes_the_payload(users_client):
    payload = {"name": "Ajinkya", "job": "SDET"}

    response = users_client.create_user(payload=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Ajinkya"
