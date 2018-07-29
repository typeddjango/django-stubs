from django.contrib.sessions.backends.db import SessionStore
from typing import Type

class Session:
    @classmethod
    def get_session_store_class(cls) -> Type[SessionStore]: ...
