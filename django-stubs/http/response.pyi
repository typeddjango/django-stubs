import functools
import io
import tempfile
from datetime import datetime
from io import BufferedReader, BytesIO
from tempfile import _TemporaryFileWrapper
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from http import cookies

from django.core.files.base import ContentFile
from django.core.handlers.wsgi import WSGIRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.template import Template
from django.template.context import Context
from django.test import Client
from django.test.client import FakePayload
from django.urls import ResolverMatch


class BadHeaderError(ValueError): ...

class HttpResponseBase:
    status_code: int = ...
    cookies: cookies.SimpleCookie = ...
    closed: bool = ...
    def __init__(
        self,
        content_type: Optional[str] = ...,
        status: Any = ...,
        reason: Optional[str] = ...,
        charset: Optional[str] = ...,
    ) -> None: ...
    @property
    def reason_phrase(self): ...
    @reason_phrase.setter
    def reason_phrase(self, value: Any) -> None: ...
    @property
    def charset(self): ...
    @charset.setter
    def charset(self, value: Any) -> None: ...
    def serialize_headers(self) -> bytes: ...
    __bytes__: Any = ...
    def __setitem__(
        self, header: Union[bytes, str], value: Union[bytes, int, str]
    ) -> None: ...
    def __delitem__(self, header: str) -> None: ...
    def __getitem__(self, header: str) -> str: ...
    def has_header(self, header: str) -> bool: ...
    __contains__: Any = ...
    def items(self): ...
    def get(
        self, header: str, alternate: Optional[Union[Tuple, str]] = ...
    ) -> Optional[Union[Tuple, str]]: ...
    def set_cookie(
        self,
        key: str,
        value: str = ...,
        max_age: Optional[int] = ...,
        expires: Optional[Union[datetime, str]] = ...,
        path: str = ...,
        domain: Optional[str] = ...,
        secure: Optional[bool] = ...,
        httponly: Optional[bool] = ...,
        samesite: Optional[str] = ...,
    ) -> None: ...
    def setdefault(self, key: str, value: str) -> None: ...
    def set_signed_cookie(
        self, key: str, value: str, salt: str = ..., **kwargs: Any
    ) -> None: ...
    def delete_cookie(
        self, key: str, path: str = ..., domain: Optional[str] = ...
    ) -> None: ...
    def make_bytes(self, value: Union[bytes, int, str]) -> bytes: ...
    def close(self) -> None: ...
    def write(self, content: str) -> Any: ...
    def flush(self) -> None: ...
    def tell(self) -> Any: ...
    def readable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def writable(self) -> bool: ...
    def writelines(self, lines: List[str]) -> Any: ...

class HttpResponse(HttpResponseBase):
    client: Client
    closed: bool
    context: Optional[Context]
    cookies: cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    redirect_chain: List[Tuple[str, int]]
    request: Dict[str, Union[FakePayload, int, str]]
    resolver_match: ResolverMatch
    sameorigin: bool
    status_code: int
    templates: List[Template]
    test_server_port: str
    test_was_secure_request: bool
    wsgi_request: WSGIRequest
    xframe_options_exempt: bool
    streaming: bool = ...
    content: Any = ...
    def __init__(
        self, content: Any = ..., *args: Any, **kwargs: Any
    ) -> None: ...
    def serialize(self): ...
    __bytes__: Any = ...
    @property
    def content(self): ...
    @content.setter
    def content(self, value: Any) -> None: ...
    def __iter__(self): ...
    def write(self, content: Union[bytes, str]) -> None: ...
    def tell(self) -> int: ...
    def getvalue(self) -> bytes: ...
    def writable(self) -> bool: ...
    def writelines(self, lines: List[str]) -> None: ...

class StreamingHttpResponse(HttpResponseBase):
    client: Client
    closed: bool
    context: None
    cookies: cookies.SimpleCookie
    json: functools.partial
    request: Dict[str, Union[FakePayload, int, str]]
    resolver_match: ResolverMatch
    status_code: int
    templates: List[Any]
    wsgi_request: WSGIRequest
    streaming: bool = ...
    streaming_content: Any = ...
    def __init__(
        self, streaming_content: Any = ..., *args: Any, **kwargs: Any
    ) -> None: ...
    @property
    def content(self) -> Any: ...
    @property
    def streaming_content(self): ...
    @streaming_content.setter
    def streaming_content(self, value: Any) -> None: ...
    def __iter__(self) -> map: ...
    def getvalue(self) -> bytes: ...

class FileResponse(StreamingHttpResponse):
    client: Client
    closed: bool
    context: None
    cookies: cookies.SimpleCookie
    file_to_stream: Optional[
        Union[
            io.BufferedReader,
            io.BytesIO,
            ContentFile,
            tempfile._TemporaryFileWrapper,
        ]
    ]
    json: functools.partial
    request: Dict[str, str]
    resolver_match: ResolverMatch
    templates: List[Any]
    wsgi_request: WSGIRequest
    block_size: int = ...
    as_attachment: bool = ...
    filename: str = ...
    def __init__(
        self,
        *args: Any,
        as_attachment: bool = ...,
        filename: str = ...,
        **kwargs: Any
    ) -> None: ...
    def set_headers(
        self,
        filelike: Union[
            BufferedReader, BytesIO, ContentFile, _TemporaryFileWrapper
        ],
    ) -> None: ...

class HttpResponseRedirectBase(HttpResponse):
    allowed_schemes: Any = ...
    def __init__(self, redirect_to: str, *args: Any, **kwargs: Any) -> None: ...
    url: Any = ...

class HttpResponseRedirect(HttpResponseRedirectBase):
    client: Client
    closed: bool
    context: Optional[Context]
    cookies: cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    redirect_chain: List[Tuple[str, int]]
    request: Dict[
        str, Union[Dict[str, str], FakePayload, int, str]
    ]
    resolver_match: ResolverMatch
    templates: List[Template]
    wsgi_request: WSGIRequest
    status_code: int = ...

class HttpResponsePermanentRedirect(HttpResponseRedirectBase):
    client: Client
    closed: bool
    context: None
    cookies: cookies.SimpleCookie
    json: functools.partial
    redirect_chain: List[Tuple[str, int]]
    request: Dict[str, str]
    resolver_match: ResolverMatch
    templates: List[Any]
    wsgi_request: WSGIRequest
    status_code: int = ...

class HttpResponseNotModified(HttpResponse):
    closed: bool
    cookies: cookies.SimpleCookie
    wsgi_request: WSGIRequest
    status_code: int = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def content(self, value: Any) -> None: ...

class HttpResponseBadRequest(HttpResponse):
    closed: bool
    cookies: cookies.SimpleCookie
    wsgi_request: WSGIRequest
    status_code: int = ...

class HttpResponseNotFound(HttpResponse):
    client: Client
    closed: bool
    context: Optional[Context]
    cookies: cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    request: Dict[str, str]
    resolver_match: ResolverMatch
    templates: List[Template]
    wsgi_request: WSGIRequest
    status_code: int = ...

class HttpResponseForbidden(HttpResponse):
    client: Client
    closed: bool
    context: Optional[Context]
    cookies: cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    request: Dict[str, Union[FakePayload, int, str]]
    resolver_match: ResolverMatch
    templates: List[Template]
    wsgi_request: WSGIRequest
    status_code: int = ...

class HttpResponseNotAllowed(HttpResponse):
    closed: bool
    cookies: cookies.SimpleCookie
    status_code: int = ...
    def __init__(
        self,
        permitted_methods: Union[List[str], Tuple[str, str]],
        *args: Any,
        **kwargs: Any
    ) -> None: ...

class HttpResponseGone(HttpResponse):
    closed: bool
    cookies: cookies.SimpleCookie
    wsgi_request: WSGIRequest
    status_code: int = ...

class HttpResponseServerError(HttpResponse):
    client: Client
    closed: bool
    context: Context
    cookies: cookies.SimpleCookie
    csrf_cookie_set: bool
    json: functools.partial
    request: Dict[str, str]
    resolver_match: ResolverMatch
    templates: List[Template]
    wsgi_request: WSGIRequest
    status_code: int = ...

class Http404(Exception): ...

class JsonResponse(HttpResponse):
    client: Client
    closed: bool
    context: None
    cookies: cookies.SimpleCookie
    json: functools.partial
    request: Dict[str, Union[FakePayload, int, str]]
    resolver_match: ResolverMatch
    status_code: int
    templates: List[Any]
    wsgi_request: WSGIRequest
    def __init__(
        self,
        data: Any,
        encoder: Type[DjangoJSONEncoder] = ...,
        safe: bool = ...,
        json_dumps_params: Optional[Dict[str, int]] = ...,
        **kwargs: Any
    ) -> None: ...
