from django.contrib.messages.storage.base import BaseStorage
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from typing import (
    Optional,
    Union,
)


def add_message(
    request: Optional[WSGIRequest],
    level: int,
    message: str,
    extra_tags: str = ...,
    fail_silently: Union[str, bool] = ...
) -> None: ...


def debug(
    request: WSGIRequest,
    message: str,
    extra_tags: str = ...,
    fail_silently: Union[str, bool] = ...
) -> None: ...


def error(
    request: WSGIRequest,
    message: str,
    extra_tags: str = ...,
    fail_silently: Union[str, bool] = ...
) -> None: ...


def get_level(request: HttpRequest) -> int: ...


def get_messages(request: HttpRequest) -> BaseStorage: ...


def info(
    request: WSGIRequest,
    message: str,
    extra_tags: str = ...,
    fail_silently: Union[str, bool] = ...
) -> None: ...


def set_level(request: HttpRequest, level: int) -> bool: ...


def success(
    request: WSGIRequest,
    message: str,
    extra_tags: str = ...,
    fail_silently: Union[str, bool] = ...
) -> None: ...


def warning(
    request: WSGIRequest,
    message: str,
    extra_tags: str = ...,
    fail_silently: Union[str, bool] = ...
) -> None: ...