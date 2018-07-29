from django.middleware.cache import CacheMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from typing import (
    Any,
    Callable,
    Tuple,
    Type,
    Union,
)


def _multi_decorate(decorators: Union[Tuple[Callable, Callable], Callable], method: Callable) -> Callable: ...


def _update_method_wrapper(_wrapper: Callable, decorator: Callable) -> None: ...


def decorator_from_middleware(middleware_class: Type[CsrfViewMiddleware]) -> Callable: ...


def decorator_from_middleware_with_args(middleware_class: Type[CacheMiddleware]) -> Callable: ...


def make_middleware_decorator(middleware_class: Any) -> Callable: ...


def method_decorator(decorator: Callable, name: str = ...) -> Callable: ...


class classonlymethod:
    def __get__(self, instance: None, cls: Any = ...) -> Callable: ...


class classproperty:
    def __get__(self, instance: Any, cls: Any = ...) -> str: ...
    def __init__(self, method: Callable = ...) -> None: ...
    def getter(self, method: Callable) -> classproperty: ...