from dispatch.tests import Callable
from functools import partial
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    Union,
)


class Signal:
    def __init__(self, providing_args: List[str] = ..., use_caching: bool = ...) -> None: ...
    def _clear_dead_receivers(self) -> None: ...
    def _live_receivers(
        self,
        sender: object
    ) -> Union[List[Callable], List[object], List[Callable], List[partial]]: ...
    def _remove_receiver(self, receiver: None = ...) -> None: ...
    def connect(
        self,
        receiver: Callable,
        sender: Any = ...,
        weak: bool = ...,
        dispatch_uid: Optional[str] = ...
    ) -> None: ...
    def disconnect(
        self,
        receiver: Optional[Callable] = ...,
        sender: Any = ...,
        dispatch_uid: Optional[str] = ...
    ) -> bool: ...
    def has_listeners(self, sender: object = ...) -> bool: ...
    def send(self, sender: Any, **named) -> Union[List[Tuple[Callable, None]], List[Tuple[object, None]]]: ...