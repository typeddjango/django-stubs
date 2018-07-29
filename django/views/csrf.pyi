from django.http.request import HttpRequest
from django.http.response import HttpResponseForbidden


def csrf_failure(
    request: HttpRequest,
    reason: str = ...,
    template_name: str = ...
) -> HttpResponseForbidden: ...