from typing import Any, Iterator, List, Optional, Union

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage


class EmailBackend(BaseEmailBackend):
    fail_silently: bool
    stream: _io.StringIO = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def write_message(self, message: EmailMessage) -> None: ...
    def send_messages(
        self, email_messages: Union[Iterator[Any], List[EmailMessage]]
    ) -> int: ...
