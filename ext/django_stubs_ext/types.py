from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from typing_extensions import override

if TYPE_CHECKING:
    from django.http.request import HttpRequest, QueryDict

    class MutableHttpRequest(HttpRequest):
        """A request with mutable query dictionaries, as used in tests."""

        GET: QueryDict  # type: ignore[assignment]
        POST: QueryDict  # type: ignore[assignment]
else:
    # The runtime class is Django's regular HttpRequest; mutability is a type-checking distinction only.
    from django.http import HttpRequest

    MutableHttpRequest = HttpRequest


# Used internally by mypy_django_plugin.
class AnyAttrAllowed(Protocol):
    def __getattr__(self, item: str) -> Any: ...

    @override
    def __setattr__(self, item: str, value: Any) -> None: ...
