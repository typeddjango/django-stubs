from typing import Any, Callable, List, Optional, Tuple, Type, Union

from django.apps.config import AppConfig
from django.conf import Settings, UserSettingsHolder
from django.core.handlers.wsgi import WSGIHandler
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.template.base import Template
from django.test.client import ClientHandler
from django.test.testcases import SimpleTestCase

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
        receiver: Any,
        sender: Optional[
            Union[Type[Union[Any, Model]], AppConfig, SimpleTestCase]
        ] = ...,
        weak: bool = ...,
        dispatch_uid: Optional[str] = ...,
    ) -> None: ...
    def disconnect(
        self,
        receiver: Optional[Callable] = ...,
        sender: Optional[
            Union[Type[Union[Any, Model]], AppConfig, SimpleTestCase]
        ] = ...,
        dispatch_uid: Optional[str] = ...,
    ) -> bool: ...
    def has_listeners(self, sender: Any = ...) -> bool: ...
    def send(
        self,
        sender: Optional[
            Union[
                Type[
                    Optional[
                        Union[
                            Settings,
                            UserSettingsHolder,
                            WSGIHandler,
                            DatabaseWrapper,
                            Model,
                            ClientHandler,
                            SimpleTestCase,
                        ]
                    ]
                ],
                AppConfig,
                Template,
                SimpleTestCase,
                str,
            ]
        ],
        **named: Any
    ) -> List[Tuple[Optional[str], Optional[str]]]: ...
    def send_robust(
        self, sender: SimpleTestCase, **named: Any
    ) -> List[Tuple[Callable, Union[ValueError, str]]]: ...

def receiver(
    signal: Union[List[Signal], Signal], **kwargs: Any
) -> Callable: ...
