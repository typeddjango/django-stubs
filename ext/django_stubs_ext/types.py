from typing import Any, Protocol

from typing_extensions import override


# Used internally by mypy_django_plugin.
class AnyAttrAllowed(Protocol):
    def __getattr__(self, item: str) -> Any: ...

    @override
    def __setattr__(self, item: str, value: Any) -> None: ...
