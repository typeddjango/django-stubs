from typing import Any, List, Optional, Tuple

from .message import DEFAULT_ATTACHMENT_MIME_TYPE as DEFAULT_ATTACHMENT_MIME_TYPE
from .message import BadHeaderError as BadHeaderError
from .message import EmailMessage as EmailMessage
from .message import EmailMultiAlternatives as EmailMultiAlternatives
from .message import SafeMIMEMultipart as SafeMIMEMultipart
from .message import SafeMIMEText as SafeMIMEText
from .message import forbid_multi_line_headers as forbid_multi_line_headers
from .utils import DNS_NAME as DNS_NAME
from .utils import CachedDnsName as CachedDnsName

def get_connection(backend: Optional[str] = ..., fail_silently: bool = ..., **kwds: Any) -> Any: ...
def send_mail(
    subject: str,
    message: str,
    from_email: Optional[str],
    recipient_list: List[str],
    fail_silently: bool = ...,
    auth_user: Optional[str] = ...,
    auth_password: Optional[str] = ...,
    connection: Optional[Any] = ...,
    html_message: Optional[str] = ...,
) -> int: ...
def send_mass_mail(
    datatuple: List[Tuple[str, str, str, List[str]]],
    fail_silently: bool = ...,
    auth_user: Optional[str] = ...,
    auth_password: Optional[str] = ...,
    connection: Optional[Any] = ...,
) -> int: ...
def mail_admins(
    subject: str,
    message: str,
    fail_silently: bool = ...,
    connection: Optional[Any] = ...,
    html_message: Optional[str] = ...,
) -> None: ...
def mail_managers(
    subject: str,
    message: str,
    fail_silently: bool = ...,
    connection: Optional[Any] = ...,
    html_message: Optional[str] = ...,
) -> None: ...

outbox: List[EmailMessage] = ...
