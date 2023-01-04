from datetime import datetime
from typing import Any, TypeVar

from django.contrib.sessions.backends.base import SessionBase
from django.db import models

_T = TypeVar("_T", bound=AbstractBaseSession)

class BaseSessionManager(models.Manager[_T]):
    def encode(self, session_dict: dict[str, Any]) -> str: ...
    def save(self, session_key: str, session_dict: dict[str, Any], expire_date: datetime) -> _T: ...

class AbstractBaseSession(models.Model):
    expire_date: datetime
    session_data: str
    session_key: str
    objects: Any
    @classmethod
    def get_session_store_class(cls) -> type[SessionBase] | None: ...
    def get_decoded(self) -> dict[str, Any]: ...
