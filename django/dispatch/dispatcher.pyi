from django.db.models.base import Model
from functools import partial
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)


class Signal:
    def __init__(self, providing_args: List[str] = ..., use_caching: bool = ...) -> None: ...
    def _clear_dead_receivers(self) -> None: ...
    def _live_receivers(self, sender: object) -> Union[List[partial], List[Callable], List[object]]: ...
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
    def send(
        self,
        sender: Type[Model],
        **named
    ) -> Union[List[Tuple[object, None]], List[Tuple[Callable, None]]]: ...