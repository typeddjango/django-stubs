from typing import Any, Generic

from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.base_session import AbstractBaseSession
from django.utils.functional import cached_property
from typing_extensions import TypeVar

_SessionT = TypeVar("_SessionT", bound=AbstractBaseSession, default=AbstractBaseSession)

class SessionStore(SessionBase, Generic[_SessionT]):
    def __init__(self, session_key: str | None = None) -> None: ...
    @classmethod
    def get_model_class(cls) -> type[_SessionT]: ...
    @cached_property
    def model(self) -> type[_SessionT]: ...
    def create_model_instance(self, data: dict[str, Any]) -> _SessionT: ...
    async def acreate_model_instance(self, data: dict[str, Any]) -> _SessionT: ...
