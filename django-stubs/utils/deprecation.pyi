from collections.abc import Callable
from typing import Any, Protocol

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from typing_extensions import TypeAlias

class RemovedInDjango40Warning(DeprecationWarning): ...
class RemovedInDjango41Warning(PendingDeprecationWarning): ...

RemovedInNextVersionWarning: TypeAlias = RemovedInDjango40Warning

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

class GetResponseCallable(Protocol):
    def __call__(self, __request: HttpRequest) -> HttpResponse: ...

class MiddlewareMixin:
    get_response: GetResponseCallable
    def __init__(self, get_response: GetResponseCallable = ...) -> None: ...
    def __call__(self, request: HttpRequest) -> HttpResponse: ...
