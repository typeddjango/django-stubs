from django.core.exceptions import (
    PermissionDenied,
    SuspiciousOperation,
)
from django.core.handlers.wsgi import WSGIRequest
from django.http.multipartparser import MultiPartParserError
from django.http.response import (
    Http404,
    HttpResponse,
)
from django.urls.resolvers import URLResolver
from typing import (
    Callable,
    Union,
)


def convert_exception_to_response(get_response: Callable) -> Callable: ...


def get_exception_response(
    request: WSGIRequest,
    resolver: URLResolver,
    status_code: int,
    exception: Union[MultiPartParserError, PermissionDenied, Http404, SuspiciousOperation],
    sender: None = ...
) -> HttpResponse: ...


def response_for_exception(
    request: WSGIRequest,
    exc: Exception
) -> HttpResponse: ...