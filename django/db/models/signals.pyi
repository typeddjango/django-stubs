from django.apps.registry import Apps
from typing import (
    Any,
    Callable,
    Optional,
)


class ModelSignal:
    def _lazy_method(
        self,
        method: Callable,
        apps: Optional[Apps],
        receiver: Callable,
        sender: Any,
        **kwargs
    ) -> Optional[bool]: ...
    def connect(
        self,
        receiver: Callable,
        sender: Any = ...,
        weak: bool = ...,
        dispatch_uid: None = ...,
        apps: None = ...
    ) -> None: ...
    def disconnect(
        self,
        receiver: Callable = ...,
        sender: Any = ...,
        dispatch_uid: None = ...,
        apps: None = ...
    ) -> bool: ...