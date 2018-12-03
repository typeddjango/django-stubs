from typing import Any, List, Optional, Tuple

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE as DEFAULT_ATTACHMENT_MIME_TYPE
from django.core.mail.message import BadHeaderError as BadHeaderError
from django.core.mail.message import EmailMessage as EmailMessage
from django.core.mail.message import EmailMultiAlternatives as EmailMultiAlternatives
from django.core.mail.message import SafeMIMEMultipart as SafeMIMEMultipart
from django.core.mail.message import SafeMIMEText as SafeMIMEText
from django.core.mail.message import forbid_multi_line_headers as forbid_multi_line_headers
from django.core.mail.message import make_msgid as make_msgid
from django.core.mail.utils import DNS_NAME as DNS_NAME
from django.core.mail.utils import CachedDnsName as CachedDnsName

def get_connection(backend: Optional[str] = ..., fail_silently: bool = ..., **kwds: Any) -> BaseEmailBackend: ...
def send_mail(
    subject: str,
    message: str,
    from_email: Optional[str],
    recipient_list: List[str],
    fail_silently: bool = ...,
    auth_user: None = ...,
    auth_password: None = ...,
    connection: Optional[BaseEmailBackend] = ...,
    html_message: Optional[str] = ...,
) -> int: ...
def send_mass_mail(
    datatuple: List[Tuple[str, str, str, List[str]]],
    fail_silently: bool = ...,
    auth_user: None = ...,
    auth_password: None = ...,
    connection: BaseEmailBackend = ...,
) -> int: ...
def mail_admins(
    subject: str,
    message: str,
    fail_silently: bool = ...,
    connection: Optional[BaseEmailBackend] = ...,
    html_message: Optional[str] = ...,
) -> None: ...
def mail_managers(
    subject: str,
    message: str,
    fail_silently: bool = ...,
    connection: Optional[BaseEmailBackend] = ...,
    html_message: Optional[str] = ...,
) -> None: ...
