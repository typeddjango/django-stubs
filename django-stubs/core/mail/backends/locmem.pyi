from typing import Any, Iterator, List, Optional, Union

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage


class EmailBackend(BaseEmailBackend):
    fail_silently: bool
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def send_messages(
        self, messages: Union[List[EmailMessage], Iterator[Any]]
    ) -> int: ...
