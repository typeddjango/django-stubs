from typing import TypeVar

from django.utils.deprecation import _AsyncGetResponseCallable, _GetResponseCallable

_ViewFuncT = TypeVar("_ViewFuncT", bound=_AsyncGetResponseCallable | _GetResponseCallable)  # noqa: PYI018
