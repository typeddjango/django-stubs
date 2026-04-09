from typing import Any, Protocol, TypeVar

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase

# `*args: Any, **kwargs: Any` means any extra argument(s) can be provided, or none.
class _View(Protocol):
    def __call__(self, request: HttpRequest, /, *args: Any, **kwargs: Any) -> HttpResponseBase: ...

class _AsyncView(Protocol):
    async def __call__(self, request: HttpRequest, /, *args: Any, **kwargs: Any) -> HttpResponseBase: ...

_ViewFuncT = TypeVar("_ViewFuncT", bound=_View | _AsyncView)  # noqa: PYI018
