from typing import ClassVar, TypeVar

from django.contrib.sessions.base_session import AbstractBaseSession, BaseSessionManager
from typing_extensions import Self

_T = TypeVar("_T", bound=Session)

class SessionManager(BaseSessionManager[_T]): ...

class Session(AbstractBaseSession):
    objects: ClassVar[SessionManager[Self]]  # type: ignore[assignment]
