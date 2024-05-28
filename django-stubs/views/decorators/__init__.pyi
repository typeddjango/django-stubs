from collections.abc import Awaitable, Callable
from typing import TypeVar

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from typing_extensions import Concatenate

# Examples:
# def (request: HttpRequest, path_param: str) -> HttpResponseBase
# async def (request: HttpRequest) -> HttpResponseBase
_ViewFuncT = TypeVar(  # noqa: PYI018
    "_ViewFuncT",
    bound=Callable[Concatenate[HttpRequest, ...], HttpResponseBase]
    | Callable[Concatenate[HttpRequest, ...], Awaitable[HttpResponseBase]],
)
