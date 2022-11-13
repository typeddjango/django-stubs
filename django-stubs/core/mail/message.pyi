from collections.abc import Sequence
from email import charset as Charset
from email._policybase import Policy
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# switch to tuple once https://github.com/python/mypy/issues/11098 is fixed
# remove Optional once python 3.7 is dropped (Tuple[str | None, ...] works with mypy on py3.10)
from typing import Any, Optional, Tuple, overload  # noqa: Y022, Y037

from typing_extensions import TypeAlias

utf8_charset: Any
utf8_charset_qp: Any
DEFAULT_ATTACHMENT_MIME_TYPE: str
RFC5322_EMAIL_LINE_LENGTH_LIMIT: int

class BadHeaderError(ValueError): ...

ADDRESS_HEADERS: set[str]

def forbid_multi_line_headers(name: str, val: str, encoding: str) -> tuple[str, str]: ...
def sanitize_address(addr: tuple[str, str] | str, encoding: str) -> str: ...

class MIMEMixin:
    def as_string(self, unixfrom: bool = ..., linesep: str = ...) -> str: ...
    def as_bytes(self, unixfrom: bool = ..., linesep: str = ...) -> bytes: ...

class SafeMIMEMessage(MIMEMixin, MIMEMessage):  # type: ignore
    defects: list[Any]
    epilogue: Any
    policy: Policy
    preamble: Any
    def __setitem__(self, name: str, val: str) -> None: ...

class SafeMIMEText(MIMEMixin, MIMEText):  # type: ignore
    defects: list[Any]
    epilogue: None
    policy: Policy
    preamble: None
    encoding: str
    def __init__(self, _text: str, _subtype: str = ..., _charset: str = ...) -> None: ...
    def __setitem__(self, name: str, val: str) -> None: ...
    def set_payload(
        self, payload: list[Message] | str | bytes, charset: str | Charset.Charset | None = ...
    ) -> None: ...

class SafeMIMEMultipart(MIMEMixin, MIMEMultipart):  # type: ignore
    defects: list[Any]
    epilogue: None
    policy: Policy
    preamble: None
    encoding: str
    def __init__(
        self,
        _subtype: str = ...,
        boundary: Any | None = ...,
        _subparts: Any | None = ...,
        encoding: str = ...,
        **_params: Any
    ) -> None: ...
    def __setitem__(self, name: str, val: str) -> None: ...

_AttachmentContent: TypeAlias = bytes | EmailMessage | Message | SafeMIMEText | str
# switch to tuple once https://github.com/python/mypy/issues/11098 is fixed
# remove Optional once python 3.7 is dropped (Tuple[str | None, ...] works with mypy on py3.10)
_AttachmentTuple: TypeAlias = (
    Tuple[str, _AttachmentContent]
    | Tuple[Optional[str], _AttachmentContent, str]
    | Tuple[str, _AttachmentContent, None]
)

class EmailMessage:
    content_subtype: str
    mixed_subtype: str
    encoding: Any
    to: list[str]
    cc: list[Any]
    bcc: list[Any]
    reply_to: list[Any]
    from_email: str
    subject: str
    body: str
    attachments: list[Any]
    extra_headers: dict[Any, Any]
    connection: Any
    def __init__(
        self,
        subject: str = ...,
        body: str | None = ...,
        from_email: str | None = ...,
        to: Sequence[str] | None = ...,
        bcc: Sequence[str] | None = ...,
        connection: Any | None = ...,
        attachments: Sequence[MIMEBase | _AttachmentTuple] | None = ...,
        headers: dict[str, str] | None = ...,
        cc: Sequence[str] | None = ...,
        reply_to: Sequence[str] | None = ...,
    ) -> None: ...
    def get_connection(self, fail_silently: bool = ...) -> Any: ...
    # TODO: when typeshed gets more types for email.Message, move it to MIMEMessage, now it has too many false-positives
    def message(self) -> Any: ...
    def recipients(self) -> list[str]: ...
    def send(self, fail_silently: bool = ...) -> int: ...
    @overload
    def attach(self, filename: MIMEBase = ..., content: None = ..., mimetype: None = ...) -> None: ...
    @overload
    def attach(self, filename: None = ..., content: _AttachmentContent = ..., mimetype: str = ...) -> None: ...
    @overload
    def attach(self, filename: str = ..., content: _AttachmentContent = ..., mimetype: str | None = ...) -> None: ...
    def attach_file(self, path: str, mimetype: str | None = ...) -> None: ...

class EmailMultiAlternatives(EmailMessage):
    alternative_subtype: str
    alternatives: list[tuple[_AttachmentContent, str]]
    def __init__(
        self,
        subject: str = ...,
        body: str | None = ...,
        from_email: str | None = ...,
        to: Sequence[str] | None = ...,
        bcc: Sequence[str] | None = ...,
        connection: Any | None = ...,
        attachments: Sequence[MIMEBase | _AttachmentTuple] | None = ...,
        headers: dict[str, str] | None = ...,
        alternatives: list[tuple[_AttachmentContent, str]] | None = ...,
        cc: Sequence[str] | None = ...,
        reply_to: Sequence[str] | None = ...,
    ) -> None: ...
    def attach_alternative(self, content: _AttachmentContent, mimetype: str) -> None: ...
