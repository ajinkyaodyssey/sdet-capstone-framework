from tests.api.builders.user_builder import UserBuilder


def test_create_user_echoes_the_payload(users_client):
    payload = UserBuilder().with_job("Lead SDET").build()

    response = users_client.create_user(payload=payload)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]
    assert response.json()["job"] == "Lead SDET"


def test_create_user_response_has_id_and_created_at(users_client):
    payload = UserBuilder().build()

    response = users_client.create_user(payload=payload)

    body = response.json()
    assert response.status_code == 201
    assert "id" in body
    assert "createdAt" in body


def test_update_user_returns_new_job_and_updated_at(users_client):
    payload = UserBuilder().with_job("Lead SDET").build()

    response = users_client.update_user(user_id=2, payload=payload)

    body = response.json()
    assert response.status_code == 200
    assert body["job"] == "Lead SDET"
    assert "updatedAt" in body


def test_patch_user_changes_only_the_job(users_client):
    response = users_client.update_user(user_id=2, payload={"job": "Senior SDET"})

    assert response.status_code == 200
    assert response.json()["job"] == "Senior SDET"


def test_delete_user_returns_204_and_empty_body(users_client):
    response = users_client.delete_user(user_id=2)

    assert response.status_code == 204
    assert response.text == ""


def test_created_user_fixture_provides_an_id(created_user):
    assert created_user["id"]
