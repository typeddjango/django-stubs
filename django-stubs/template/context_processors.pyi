from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.utils.functional import SimpleLazyObject
from typing import (
    Callable,
    Dict,
    List,
    Tuple,
    Union,
)


def csrf(request: HttpRequest) -> Dict[str, SimpleLazyObject]: ...


def debug(request: HttpRequest) -> Dict[str, Union[bool, Callable]]: ...


def i18n(request: WSGIRequest) -> Dict[str, Union[List[Tuple[str, str]], str, bool]]: ...


def request(request: HttpRequest) -> Dict[str, HttpRequest]: ...