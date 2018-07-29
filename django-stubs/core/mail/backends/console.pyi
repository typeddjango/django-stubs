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
        email_messages: Union[List[EmailMultiAlternatives], List[EmailMessage]]
    ) -> int: ...
    def write_message(self, message: EmailMultiAlternatives) -> None: ...