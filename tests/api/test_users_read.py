import jsonschema
from tests.api.schemas import USER_SCHEMA


def test_list_users_page_one_returns_users(users_client):
    response = users_client.list_users(1)

    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


def test_page_two_has_different_users_than_page_one(users_client):
    first = users_client.list_users(page=1).json()["data"]
    second = users_client.list_users(page=2).json()["data"]

    first_ids = {user["id"] for user in first}
    second_ids = {user["id"] for user in second}

    assert first_ids.isdisjoint(second_ids)


def test_per_page_limits_the_number_of_users(users_client):
    response = users_client.list_users(page=1, per_page=3)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 3


def test_get_user_returns_that_user_quickly(users_client):
    response = users_client.get_user(user_id=2)

    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.elapsed.total_seconds() < 3


def test_get_user_matches_schema(users_client):
    my_response = users_client.get_user(user_id=2)

    assert my_response.status_code == 200
    jsonschema.validate(instance=my_response.json()["data"], schema=USER_SCHEMA)


def test_unknown_user_gets_404(users_client):
    my_response = users_client.get_user(user_id=299)

    assert my_response.status_code == 404
    assert my_response.json() == {}
