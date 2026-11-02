from typing import Any

import requests

from tests.api.clients.base_client import BaseClient


class UsersClient(BaseClient):
    _USERS = "/users"

    def list_users(self, page: int = 1, per_page: int = 6) -> requests.Response:
        params = {"page": page, "per_page": per_page}
        return self.get(self._USERS, params=params)

    def get_user(self, user_id: int | str) -> requests.Response:
        return self.get(f"{self._USERS}/{user_id}")

    def create_user(self, payload: dict[str, Any]) -> requests.Response:
        return self.post(self._USERS, json=payload)

    def update_user(self, user_id: int | str, payload: dict[str, Any]) -> requests.Response:
        return self.put(f"{self._USERS}/{user_id}", json=payload)

    def delete_user(self, user_id: int | str) -> requests.Response:
        return self.delete(f"{self._USERS}/{user_id}")
