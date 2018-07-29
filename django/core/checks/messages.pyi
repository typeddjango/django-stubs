from typing import (
    Any,
    Optional,
)


class CheckMessage:
    def __eq__(self, other: CheckMessage) -> bool: ...
    def __init__(
        self,
        level: int,
        msg: str,
        hint: Optional[str] = ...,
        obj: Any = ...,
        id: Optional[str] = ...
    ) -> None: ...
    def __str__(self) -> str: ...
    def is_serious(self, level: int = ...) -> bool: ...
    def is_silenced(self) -> bool: ...


class Critical:
    def __init__(self, *args, **kwargs) -> None: ...


class Error:
    def __init__(self, *args, **kwargs) -> None: ...


class Warning:
    def __init__(self, *args, **kwargs) -> None: ...