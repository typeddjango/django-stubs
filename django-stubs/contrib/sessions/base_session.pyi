from datetime import date, datetime
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
    session_key: models.CharField[str | int | Combinable | None, str]
    # 'session_key' is declared as primary key
    pk: models.CharField[str | int | Combinable | None, str]
    session_data: models.TextField[str | int | Combinable, str]
    expire_date: models.DateTimeField[str | datetime | date | Combinable, datetime]
    objects: ClassVar[BaseSessionManager[Self]]

    @classmethod
    def get_session_store_class(cls) -> type[SessionBase] | None: ...
    def get_decoded(self) -> dict[str, Any]: ...
