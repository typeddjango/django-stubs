from django.http import HttpRequest, HttpResponse
from django.views.decorators.csp import csp_override, csp_report_only_override
from typing_extensions import assert_type


@csp_override(
    {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "report-uri": "/path/to/reports-endpoint/",
    }
)
def my_view(request: HttpRequest) -> HttpResponse: ...


@csp_report_only_override(
    {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "report-uri": "/path/to/reports-endpoint/",
    }
)
def my_view2(request: HttpRequest) -> HttpResponse: ...


assert_type(my_view(HttpRequest()), HttpResponse)
assert_type(my_view2(HttpRequest()), HttpResponse)
