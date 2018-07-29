from django.core.mail.backends.base import BaseEmailBackend
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def forbid_multi_line_headers(name: str, val: str, encoding: str) -> Tuple[str, str]: ...


def sanitize_address(addr: Union[str, Tuple[str, str]], encoding: str) -> str: ...


def split_addr(addr: str, encoding: str) -> Tuple[str, str]: ...


class EmailMessage:
    def __init__(
        self,
        subject: str = ...,
        body: str = ...,
        from_email: Optional[str] = ...,
        to: Optional[List[str]] = ...,
        bcc: None = ...,
        connection: Any = ...,
        attachments: Optional[List[MIMEText]] = ...,
        headers: Optional[Dict[str, str]] = ...,
        cc: Optional[List[str]] = ...,
        reply_to: Optional[List[str]] = ...
    ) -> None: ...
    def _create_attachment(
        self,
        filename: Optional[str],
        content: Union[str, bytes, SafeMIMEText],
        mimetype: str = ...
    ) -> MIMEBase: ...
    def _create_attachments(
        self,
        msg: Union[SafeMIMEMultipart, SafeMIMEText]
    ) -> Union[SafeMIMEMultipart, SafeMIMEText]: ...
    def _create_message(
        self,
        msg: SafeMIMEText
    ) -> Union[SafeMIMEMultipart, SafeMIMEText]: ...
    def _create_mime_attachment(self, content: Union[str, bytes], mimetype: str) -> MIMEBase: ...
    def _set_list_header_if_not_empty(
        self,
        msg: Union[SafeMIMEMultipart, SafeMIMEText],
        header: str,
        values: List[str]
    ) -> None: ...
    def attach(self, filename: str = ..., content: bytes = ..., mimetype: Optional[str] = ...) -> None: ...
    def attach_file(self, path: str, mimetype: Optional[str] = ...) -> None: ...
    def get_connection(self, fail_silently: bool = ...) -> BaseEmailBackend: ...
    def message(self) -> Union[SafeMIMEMultipart, SafeMIMEText]: ...
    def recipients(self) -> List[str]: ...
    def send(self, fail_silently: bool = ...) -> int: ...


class EmailMultiAlternatives:
    def __init__(
        self,
        subject: str = ...,
        body: str = ...,
        from_email: Optional[str] = ...,
        to: List[str] = ...,
        bcc: None = ...,
        connection: Any = ...,
        attachments: None = ...,
        headers: Optional[Dict[str, str]] = ...,
        alternatives: None = ...,
        cc: None = ...,
        reply_to: None = ...
    ) -> None: ...
    def _create_alternatives(
        self,
        msg: SafeMIMEText
    ) -> Union[SafeMIMEMultipart, SafeMIMEText]: ...
    def _create_message(
        self,
        msg: SafeMIMEText
    ) -> Union[SafeMIMEMultipart, SafeMIMEText]: ...
    def attach_alternative(self, content: str, mimetype: str) -> None: ...


class MIMEMixin:
    def as_bytes(self, unixfrom: bool = ..., linesep: str = ...) -> bytes: ...
    def as_string(self, unixfrom: bool = ..., linesep: str = ...) -> str: ...


class SafeMIMEMessage:
    def __setitem__(self, name: str, val: str) -> None: ...


class SafeMIMEMultipart:
    def __init__(
        self,
        _subtype: str = ...,
        boundary: None = ...,
        _subparts: None = ...,
        encoding: str = ...,
        **_params
    ) -> None: ...
    def __setitem__(self, name: str, val: str) -> None: ...


class SafeMIMEText:
    def __init__(self, _text: str, _subtype: str = ..., _charset: str = ...) -> None: ...
    def __setitem__(self, name: str, val: str) -> None: ...
    def set_payload(self, payload: str, charset: str = ...) -> None: ...