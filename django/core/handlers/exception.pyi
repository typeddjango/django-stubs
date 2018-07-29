from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.urls.resolvers import URLResolver
from typing import Callable


def convert_exception_to_response(get_response: Callable) -> Callable: ...


def get_exception_response(
    request: WSGIRequest,
    resolver: URLResolver,
    status_code: int,
    exception: Exception,
    sender: None = ...
) -> HttpResponse: ...


def response_for_exception(
    request: WSGIRequest,
    exc: Exception
) -> HttpResponse: ...