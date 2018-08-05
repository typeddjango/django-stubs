from typing import Any, Callable, List, Optional, Tuple, Type, Union

from django.apps.config import AppConfig
from django.conf import Settings, UserSettingsHolder
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.template.base import Template

NONE_ID: Any
NO_RECEIVERS: Any

class Signal:
    receivers: Any = ...
    providing_args: Any = ...
    lock: Any = ...
    use_caching: Any = ...
    sender_receivers_cache: Any = ...
    def __init__(
        self, providing_args: List[str] = ..., use_caching: bool = ...
    ) -> None: ...
    def connect(
        self,
        receiver: Callable,
        sender: Optional[Union[Type[Model], AppConfig]] = ...,
        weak: bool = ...,
        dispatch_uid: Optional[str] = ...,
    ) -> None: ...
    def disconnect(
        self,
        receiver: Optional[Callable] = ...,
        sender: None = ...,
        dispatch_uid: Optional[str] = ...,
    ) -> bool: ...
    def has_listeners(self, sender: Type[Model] = ...) -> bool: ...
    def send(
        self,
        sender: Optional[
            Union[
                Type[
                    Union[Model, UserSettingsHolder, DatabaseWrapper, Settings]
                ],
                AppConfig,
                Template,
            ]
        ],
        **named: Any
    ) -> List[Tuple[Callable, None]]: ...
    def send_robust(self, sender: Any, **named: Any): ...

def receiver(signal: Signal, **kwargs: Any) -> Callable: ...
