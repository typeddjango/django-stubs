from typing import Any, Optional, Type

from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.base_session import AbstractBaseSession, BaseSessionManager

class SessionManager(BaseSessionManager):
    creation_counter: int
    model: None
    name: None
    use_in_migrations: bool = ...

class Session(AbstractBaseSession):
    expire_date: datetime.datetime
    session_data: str
    session_key: str
    objects: Any = ...
    @classmethod
    def get_session_store_class(cls) -> Type[SessionStore]: ...
