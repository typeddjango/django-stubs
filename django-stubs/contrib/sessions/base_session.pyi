from datetime import datetime
from typing import Any, ClassVar, TypeVar

from django.contrib.sessions.backends.base import SessionBase
from django.db import models
from django.db.models.expressions import Combinable
from typing_extensions import Self

_T = TypeVar("_T", bound=AbstractBaseSession)

class BaseSessionManager(models.Manager[_T]):
    def encode(self, session_dict: dict[str, Any]) -> str: ...
    def save(self, session_key: str, session_dict: dict[str, Any], expire_date: datetime) -> _T: ...

class AbstractBaseSession(models.Model):
    pk: models.CharField[str | int | Combinable | None, str]
    session_key = models.CharField[str | int | Combinable | None, str](primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    objects: ClassVar[BaseSessionManager[Self]]

    @classmethod
    def get_session_store_class(cls) -> type[SessionBase] | None: ...
    def get_decoded(self) -> dict[str, Any]: ...
