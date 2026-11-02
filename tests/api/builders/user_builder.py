import uuid
from typing import Self


class UserBuilder:
    def __init__(self) -> None:
        self._data = {
            "name": f"user_{uuid.uuid4().hex[:8]}",
            "job": "SDET",
        }

    def with_name(self, name: str) -> Self:
        self._data["name"] = name
        return self

    def with_job(self, job: str) -> Self:
        self._data["job"] = job
        return self

    def without(self, field: str) -> Self:
        self._data.pop(field, None)
        return self

    def build(self) -> dict[str, str]:
        return dict(self._data)
