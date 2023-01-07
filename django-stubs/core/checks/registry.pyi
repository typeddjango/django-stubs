from collections.abc import Callable, Iterable, Sequence
from typing import Any, Protocol, TypeVar, overload

from django.apps.config import AppConfig
from django.core.checks.messages import CheckMessage

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

class _CheckCallable(Protocol):
    def __call__(
        self,
        *,
        app_configs: Sequence[AppConfig] | None,
        databases: Sequence[str] | None,
        **kwargs: Any,
    ) -> Iterable[CheckMessage]: ...

_C = TypeVar("_C", bound=_CheckCallable)

class _ProcessedCheckCallable(Protocol[_C]):
    tags: Sequence[str]
    __call__: _C

class CheckRegistry:
    registered_checks: set[_ProcessedCheckCallable]
    deployment_checks: set[_ProcessedCheckCallable]
    def __init__(self) -> None: ...
    @overload
    def register(self, __check: _C) -> _ProcessedCheckCallable[_C]: ...
    @overload
    def register(self, *tags: str, **kwargs: Any) -> Callable[[_C], _ProcessedCheckCallable[_C]]: ...
    def run_checks(
        self,
        app_configs: Sequence[AppConfig] | None = ...,
        tags: Sequence[str] | None = ...,
        include_deployment_checks: bool = ...,
        databases: Sequence[str] | None = ...,
    ) -> list[CheckMessage]: ...
    def tag_exists(self, tag: str, include_deployment_checks: bool = ...) -> bool: ...
    def tags_available(self, deployment_checks: bool = ...) -> set[str]: ...
    def get_checks(self, include_deployment_checks: bool = ...) -> list[_ProcessedCheckCallable]: ...

registry: CheckRegistry = ...
register = registry.register
run_checks = registry.run_checks
tag_exists = registry.tag_exists
