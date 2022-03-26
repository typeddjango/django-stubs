import sys
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Type, TypeVar, Union, overload

from django.core import validators  # due to weird mypy.stubtest error
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import Storage
from django.db.models.base import Model
from django.db.models.fields import Field, _ErrorMessagesT, _FieldChoices
from django.db.models.query_utils import DeferredAttribute
from django.utils._os import _PathCompatible

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

class FieldFile(File):
    instance: Model = ...
    field: FileField = ...
    storage: Storage = ...
    name: Optional[str]
    def __init__(self, instance: Model, field: FileField, name: Optional[str]) -> None: ...
    file: Any = ...
    @property
    def path(self) -> str: ...
    @property
    def url(self) -> str: ...
    @property
    def size(self) -> int: ...
    def save(self, name: str, content: File, save: bool = ...) -> None: ...
    def delete(self, save: bool = ...) -> None: ...
    @property
    def closed(self) -> bool: ...

class FileDescriptor(DeferredAttribute):
    field: FileField = ...
    def __set__(self, instance: Model, value: Optional[Any]) -> None: ...
    def __get__(
        self, instance: Optional[Model], cls: Optional[Type[Model]] = ...
    ) -> Union[FieldFile, FileDescriptor]: ...

_T = TypeVar("_T", bound="Field")
_M = TypeVar("_M", bound=Model, contravariant=True)

class _UploadToCallable(Protocol[_M]):
    def __call__(self, __instance: _M, __filename: str) -> _PathCompatible: ...

class FileField(Field):
    storage: Storage = ...
    upload_to: Union[_PathCompatible, _UploadToCallable] = ...
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        upload_to: Union[_PathCompatible, _UploadToCallable] = ...,
        storage: Optional[Union[Storage, Callable[[], Storage]]] = ...,
        *,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner) -> FileDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner) -> Any: ...
    # non-Model instances
    @overload
    def __get__(self: _T, instance, owner) -> _T: ...
    def generate_filename(self, instance: Optional[Model], filename: _PathCompatible) -> str: ...

class ImageFileDescriptor(FileDescriptor):
    field: ImageField
    def __set__(self, instance: Model, value: Optional[str]) -> None: ...

class ImageFieldFile(ImageFile, FieldFile):
    field: ImageField
    def delete(self, save: bool = ...) -> None: ...

class ImageField(FileField):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        width_field: Optional[str] = ...,
        height_field: Optional[str] = ...,
        **kwargs: Any,
    ) -> None: ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner) -> ImageFileDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner) -> Any: ...
    # non-Model instances
    @overload
    def __get__(self: _T, instance, owner) -> _T: ...
    def update_dimension_fields(self, instance: Model, force: bool = ..., *args: Any, **kwargs: Any) -> None: ...
