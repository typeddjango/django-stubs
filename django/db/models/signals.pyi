from django.apps.registry import Apps
from django.contrib.sites.models import Site
from django.db.models.base import Model
from typing import (
    Any,
    Callable,
    Optional,
    Type,
    Union,
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
        sender: Optional[Union[Type[Site], Type[Model]]] = ...,
        weak: bool = ...,
        dispatch_uid: None = ...,
        apps: None = ...
    ) -> None: ...
    def disconnect(
        self,
        receiver: Callable = ...,
        sender: Optional[Type[Model]] = ...,
        dispatch_uid: None = ...,
        apps: None = ...
    ) -> bool: ...