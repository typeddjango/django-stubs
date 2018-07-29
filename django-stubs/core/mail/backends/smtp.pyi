from django.core.mail.message import EmailMessage
from smtplib import SMTP
from typing import (
    List,
    Optional,
    Type,
)


class EmailBackend:
    def __init__(
        self,
        host: None = ...,
        port: None = ...,
        username: Optional[str] = ...,
        password: Optional[str] = ...,
        use_tls: None = ...,
        fail_silently: bool = ...,
        use_ssl: None = ...,
        timeout: None = ...,
        ssl_keyfile: None = ...,
        ssl_certfile: None = ...,
        **kwargs
    ) -> None: ...
    def _send(self, email_message: EmailMessage) -> bool: ...
    def close(self) -> None: ...
    @property
    def connection_class(self) -> Type[SMTP]: ...
    def open(self) -> bool: ...
    def send_messages(self, email_messages: List[EmailMessage]) -> int: ...