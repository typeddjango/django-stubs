import threading
from collections.abc import Callable, MutableMapping
from logging import Logger
from typing import Any, ParamSpec, TypeVar

NONE_ID: int
NO_RECEIVERS: Any

logger: Logger

class Signal:
    receivers: list[Any]
    lock: threading.Lock
    use_caching: bool
    sender_receivers_cache: MutableMapping[Any, Any]

    def __init__(self, use_caching: bool = ...) -> None: ...
    def connect(
        self, receiver: Callable, sender: object | None = ..., weak: bool = ..., dispatch_uid: str | None = ...
    ) -> None: ...
    def disconnect(
        self, receiver: Callable | None = ..., sender: object | None = ..., dispatch_uid: str | None = ...
    ) -> bool: ...
    def has_listeners(self, sender: Any = ...) -> bool: ...
    def send(self, sender: Any, **named: Any) -> list[tuple[Callable, str | None]]: ...
    def send_robust(self, sender: Any, **named: Any) -> list[tuple[Callable, Exception | Any]]: ...
    def _live_receivers(self, sender: Any) -> list[Callable]: ...

_P = ParamSpec("_P")
_R = TypeVar("_R")

def receiver(
    signal: list[Signal] | tuple[Signal, ...] | Signal,
    *,
    sender: object | None = ...,
    weak: bool = ...,
    dispatch_uid: str | None = ...
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]: ...
