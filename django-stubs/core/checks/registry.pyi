from collections.abc import Callable, Sequence
from typing import Any, TypeVar

from django.apps.config import AppConfig
from django.core.checks.messages import CheckMessage
from typing_extensions import Protocol, TypeAlias

class Tags:
    admin: str
    caches: str
    compatibility: str
    database: str
    models: str
    security: str
    signals: str
    sites: str
    staticfiles: str
    templates: str
    translation: str
    urls: str

_CheckCallable: TypeAlias = Callable[..., Sequence[CheckMessage]]

_C = TypeVar("_C", bound=_CheckCallable)

class _ProcessedCheckCallable(Protocol[_C]):
    tags: Sequence[str]
    __call__: _C

class CheckRegistry:
    registered_checks: set[_ProcessedCheckCallable]
    deployment_checks: set[_ProcessedCheckCallable]
    def __init__(self) -> None: ...
    def register(
        self, check: _CheckCallable | str | None = ..., *tags: str, **kwargs: Any
    ) -> Callable[[_CheckCallable], _ProcessedCheckCallable] | _ProcessedCheckCallable: ...
    def run_checks(
        self,
        app_configs: Sequence[AppConfig] | None = ...,
        tags: Sequence[str] | None = ...,
        include_deployment_checks: bool = ...,
        databases: Any | None = ...,
    ) -> list[CheckMessage]: ...
    def tag_exists(self, tag: str, include_deployment_checks: bool = ...) -> bool: ...
    def tags_available(self, deployment_checks: bool = ...) -> set[str]: ...
    def get_checks(self, include_deployment_checks: bool = ...) -> list[_ProcessedCheckCallable]: ...

registry: CheckRegistry
register: Any
run_checks: Any
tag_exists: Any
