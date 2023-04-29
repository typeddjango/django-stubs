from typing import Any, Protocol


# Used internally by mypy_django_plugin.
class AnyAttrAllowed(Protocol):
    def __getattr__(self, item: str) -> Any:
        ...

    def __setattr__(self, item: str, value: Any) -> None:
        ...
