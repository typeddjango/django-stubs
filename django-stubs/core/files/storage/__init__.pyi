from typing import TypeAlias

from django.utils.functional import LazyObject

from .base import Storage
from .filesystem import FileSystemStorage
from .handler import InvalidStorageError, StorageHandler
from .memory import InMemoryStorage

__all__ = (
    "FileSystemStorage",
    "InMemoryStorage",
    "Storage",
    "DefaultStorage",
    "default_storage",
    "InvalidStorageError",
    "StorageHandler",
    "storages",
)

class DefaultStorage(LazyObject): ...

# This is our "placeholder" type the mypy plugin refines to configured
# 'STORAGES["default"]["BACKEND"]' wherever it is used as a type.
_DefaultStorage: TypeAlias = DefaultStorage

storages: StorageHandler
default_storage: _DefaultStorage
