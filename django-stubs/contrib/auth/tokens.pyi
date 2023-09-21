from datetime import date, datetime
from typing import Any

from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PasswordResetTokenGenerator:
    key_salt: str
    secret: str | bytes
    secret_fallbacks: list[str | bytes]
    algorithm: str
    def make_token(self, user: UserModel) -> str: ...
    def check_token(self, user: UserModel | None, token: str | None) -> bool: ...
    def _make_token_with_timestamp(self, user: UserModel, timestamp: int, secret: str | bytes = ...) -> str: ...
    def _make_hash_value(self, user: UserModel, timestamp: int) -> str: ...
    def _num_seconds(self, dt: datetime | date) -> int: ...
    def _now(self) -> datetime: ...

default_token_generator: Any
