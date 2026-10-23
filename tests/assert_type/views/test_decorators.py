from __future__ import annotations

from typing import assert_type

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csp import csp_override, csp_report_only_override
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, requires_csrf_token
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import conditional_page, require_GET, require_POST, require_safe


@csp_override(
    {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "report-uri": "/path/to/reports-endpoint/",
    }
)
def my_view(request: HttpRequest) -> HttpResponse:
    raise NotImplementedError


@csp_report_only_override(
    {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "report-uri": "/path/to/reports-endpoint/",
    }
)
def my_view2(request: HttpRequest) -> HttpResponse:
    raise NotImplementedError


assert_type(my_view(HttpRequest()), HttpResponse)
assert_type(my_view2(HttpRequest()), HttpResponse)


@csrf_protect
@requires_csrf_token
@ensure_csrf_cookie
def csrf_view(request: HttpRequest, pk: int) -> HttpResponse:
    raise NotImplementedError


@require_GET
@require_POST
@require_safe
@conditional_page
@gzip_page
def http_view(request: HttpRequest) -> HttpResponse:
    raise NotImplementedError


assert_type(csrf_view(HttpRequest(), 1), HttpResponse)
assert_type(http_view(HttpRequest()), HttpResponse)
