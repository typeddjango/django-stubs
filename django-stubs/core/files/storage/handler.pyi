from typing import Any, TypedDict, type_check_only

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from typing_extensions import NotRequired

from .base import Storage

@type_check_only
class _StorageConfig(TypedDict):
    BACKEND: str
    OPTIONS: NotRequired[dict[str, Any]]

class InvalidStorageError(ImproperlyConfigured): ...

class StorageHandler:
    def __init__(self, backends: dict[str, _StorageConfig] | None = None) -> None: ...
    @cached_property
    def backends(self) -> dict[str, _StorageConfig]: ...
    def __getitem__(self, alias: str) -> Storage: ...
    def create_storage(self, params: _StorageConfig) -> Storage: ...
