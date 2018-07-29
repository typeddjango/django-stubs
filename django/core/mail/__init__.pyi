from django.core.mail.backends.base import BaseEmailBackend
from typing import (
    List,
    Optional,
    Tuple,
)


def get_connection(
    backend: Optional[str] = ...,
    fail_silently: bool = ...,
    **kwds
) -> BaseEmailBackend: ...


def mail_admins(
    subject: str,
    message: str,
    fail_silently: bool = ...,
    connection: Optional[BaseEmailBackend] = ...,
    html_message: Optional[str] = ...
) -> None: ...


def mail_managers(
    subject: str,
    message: str,
    fail_silently: bool = ...,
    connection: None = ...,
    html_message: None = ...
) -> None: ...


def send_mail(
    subject: str,
    message: str,
    from_email: Optional[str],
    recipient_list: List[str],
    fail_silently: bool = ...,
    auth_user: None = ...,
    auth_password: None = ...,
    connection: Optional[BaseEmailBackend] = ...,
    html_message: Optional[str] = ...
) -> int: ...


def send_mass_mail(
    datatuple: List[Tuple[str, str, str, List[str]]],
    fail_silently: bool = ...,
    auth_user: None = ...,
    auth_password: None = ...,
    connection: BaseEmailBackend = ...
) -> int: ...