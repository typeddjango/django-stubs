from django.core.exceptions import (
    PermissionDenied,
    SuspiciousOperation,
)
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from typing import Optional


def bad_request(
    request: WSGIRequest,
    exception: SuspiciousOperation,
    template_name: str = ...
) -> HttpResponseBadRequest: ...


def page_not_found(
    request: WSGIRequest,
    exception: Optional[Http404],
    template_name: str = ...
) -> HttpResponseNotFound: ...


def permission_denied(
    request: WSGIRequest,
    exception: PermissionDenied,
    template_name: str = ...
) -> HttpResponseForbidden: ...


def server_error(
    request: WSGIRequest,
    template_name: str = ...
) -> HttpResponseServerError: ...