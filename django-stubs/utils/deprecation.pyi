from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from typing_extensions import TypeAlias

class RemovedInDjango50Warning(DeprecationWarning): ...
class RemovedInDjango51Warning(PendingDeprecationWarning): ...

RemovedInNextVersionWarning: TypeAlias = RemovedInDjango50Warning
RemovedAfterNextVersionWarning: TypeAlias = RemovedInDjango51Warning

class warn_about_renamed_method:
    class_name: str
    old_method_name: str
    new_method_name: str
    deprecation_warning: type[DeprecationWarning]
    def __init__(
        self, class_name: str, old_method_name: str, new_method_name: str, deprecation_warning: type[DeprecationWarning]
    ) -> None: ...
    def __call__(self, f: Callable) -> Callable: ...

class RenameMethodsBase(type):
    renamed_methods: Any
    def __new__(cls, name: Any, bases: Any, attrs: Any) -> type: ...

class DeprecationInstanceCheck(type):
    alternative: str
    deprecation_warning: type[Warning]
    def __instancecheck__(self, instance: Any) -> bool: ...

class _GetResponseCallable(Protocol):
    def __call__(self, __request: HttpRequest) -> HttpResponseBase: ...

class _AsyncGetResponseCallable(Protocol):
    def __call__(self, __request: HttpRequest) -> Awaitable[HttpResponseBase]: ...

class MiddlewareMixin:
    sync_capable: bool
    async_capable: bool

    get_response: _GetResponseCallable | _AsyncGetResponseCallable
    def __init__(self, get_response: _GetResponseCallable | _AsyncGetResponseCallable) -> None: ...
    def __call__(self, request: HttpRequest) -> HttpResponseBase | Awaitable[HttpResponseBase]: ...
    async def __acall__(self, request: HttpRequest) -> HttpResponseBase: ...
