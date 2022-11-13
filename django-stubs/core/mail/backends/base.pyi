from collections.abc import Sequence
from types import TracebackType
from typing import Any, TypeVar

from django.core.mail.message import EmailMessage

_T = TypeVar("_T", bound="BaseEmailBackend")

class BaseEmailBackend:
    fail_silently: bool
    def __init__(self, fail_silently: bool = ..., **kwargs: Any) -> None: ...
    def open(self) -> bool | None: ...
    def close(self) -> None: ...
    def __enter__(self: _T) -> _T: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    def send_messages(self, email_messages: Sequence[EmailMessage]) -> int: ...
