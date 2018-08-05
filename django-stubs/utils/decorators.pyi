from typing import Any, Callable, Optional, Set, Tuple, Type, Union

from django.contrib.admindocs.middleware import XViewMiddleware
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.middleware.cache import CacheMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.middleware.http import ConditionalGetMiddleware
from django.test.testcases import LiveServerTestCase
from django.views.generic.base import View


class classonlymethod(classmethod):
    def __get__(
        self,
        instance: Optional[View],
        cls: Type[
            Union[
                View,
                UserPassesTestMixin,
                PermissionRequiredMixin,
                SuccessMessageMixin,
                LoginRequiredMixin,
            ]
        ] = ...,
    ) -> Callable: ...

def method_decorator(
    decorator: Union[Callable, Tuple[Callable, Callable], Set[Callable]],
    name: str = ...,
) -> Callable: ...
def decorator_from_middleware_with_args(
    middleware_class: Type[CacheMiddleware]
) -> Callable: ...
def decorator_from_middleware(
    middleware_class: Type[
        Union[
            CsrfViewMiddleware, Any, XViewMiddleware, ConditionalGetMiddleware
        ]
    ]
) -> Callable: ...
def available_attrs(fn: Any): ...
def make_middleware_decorator(
    middleware_class: Type[
        Union[
            CsrfViewMiddleware,
            Any,
            XViewMiddleware,
            CacheMiddleware,
            ConditionalGetMiddleware,
        ]
    ]
) -> Callable: ...

class classproperty:
    fget: Optional[Callable] = ...
    def __init__(self, method: Optional[Callable] = ...) -> None: ...
    def __get__(
        self,
        instance: Optional[LiveServerTestCase],
        cls: Type[LiveServerTestCase] = ...,
    ) -> str: ...
    def getter(self, method: Callable) -> classproperty: ...
