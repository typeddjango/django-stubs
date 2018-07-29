from django.contrib.auth.mixins import PermissionRequiredMixin
from django.middleware.cache import CacheMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.test.testcases import LiveServerTestCase
from django.views.generic.base import View
from typing import (
    Callable,
    Optional,
    Tuple,
    Type,
    Union,
)


def _multi_decorate(decorators: Union[Tuple[Callable, Callable], Callable], method: Callable) -> Callable: ...


def _update_method_wrapper(_wrapper: Callable, decorator: Callable) -> None: ...


def decorator_from_middleware(middleware_class: Type[CsrfViewMiddleware]) -> Callable: ...


def decorator_from_middleware_with_args(middleware_class: Type[CacheMiddleware]) -> Callable: ...


def make_middleware_decorator(middleware_class: Type[object]) -> Callable: ...


def method_decorator(decorator: Callable, name: str = ...) -> Callable: ...


class classonlymethod:
    def __get__(
        self,
        instance: None,
        cls: Type[Union[View, PermissionRequiredMixin]] = ...
    ) -> Callable: ...


class classproperty:
    def __get__(
        self,
        instance: Optional[LiveServerTestCase],
        cls: Type[LiveServerTestCase] = ...
    ) -> str: ...
    def __init__(self, method: Callable = ...) -> None: ...
    def getter(self, method: Callable) -> classproperty: ...