from django.core.mail.message import (
    EmailMessage,
    EmailMultiAlternatives,
)
from typing import (
    List,
    Union,
)


class EmailBackend:
    def __init__(self, *args, **kwargs) -> None: ...
    def send_messages(
        self,
        messages: Union[List[EmailMultiAlternatives], List[EmailMessage]]
    ) -> int: ...