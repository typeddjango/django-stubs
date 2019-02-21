from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http.response import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)

ERROR_404_TEMPLATE_NAME: str
ERROR_403_TEMPLATE_NAME: str
ERROR_400_TEMPLATE_NAME: str
ERROR_500_TEMPLATE_NAME: str

def page_not_found(
    request: WSGIRequest, exception: Optional[Http404], template_name: str = ...
) -> HttpResponseNotFound: ...
def server_error(request: WSGIRequest, template_name: str = ...) -> HttpResponseServerError: ...
def bad_request(request: WSGIRequest, exception: Exception, template_name: str = ...) -> HttpResponseBadRequest: ...
def permission_denied(
    request: WSGIRequest, exception: Exception, template_name: str = ...
) -> HttpResponseForbidden: ...
