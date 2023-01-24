from collections.abc import Callable, Iterable
from typing import Any, AnyStr, Protocol, TypeVar, overload

from _typeshed import Self
from django.core import validators  # due to weird mypy.stubtest error
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import Storage
from django.db.models.base import Model
from django.db.models.fields import Field, _ErrorMessagesT, _FieldChoices
from django.db.models.query_utils import DeferredAttribute
from django.utils._os import _PathCompatible
from django.utils.functional import _StrOrPromise

class FieldFile(File[AnyStr]):
    instance: Model
    field: FileField
    storage: Storage
    name: str | None
    def __init__(self, instance: Model, field: FileField, name: str | None) -> None: ...
    file: Any
    @property
    def path(self) -> str: ...
    @property
    def url(self) -> str: ...
    @property
    def size(self) -> int: ...
    def save(self, name: str, content: File[AnyStr], save: bool = ...) -> None: ...
    def delete(self, save: bool = ...) -> None: ...
    @property
    def closed(self) -> bool: ...

class FileDescriptor(DeferredAttribute):
    field: FileField
    def __set__(self, instance: Model, value: Any | None) -> None: ...
    def __get__(self, instance: Model | None, cls: type[Model] | None = ...) -> FieldFile[AnyStr] | FileDescriptor: ...

_M = TypeVar("_M", bound=Model, contravariant=True)

class _UploadToCallable(Protocol[_M]):
    def __call__(self, __instance: _M, __filename: str) -> _PathCompatible: ...

class FileField(Field[Any, Any]):
    storage: Storage
    upload_to: _PathCompatible | _UploadToCallable[Model]
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        upload_to: _PathCompatible | _UploadToCallable[_M] = ...,
        storage: Storage | Callable[[], Storage] | None = ...,
        *,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _FieldChoices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesT | None = ...,
    ) -> None: ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner: Any) -> FileDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner: Any) -> Any: ...
    # non-Model instances
    @overload
    def __get__(self: Self, instance: Any, owner: Any) -> Self: ...
    def generate_filename(self, instance: Model | None, filename: _PathCompatible) -> str: ...

class ImageFileDescriptor(FileDescriptor):
    field: ImageField
    def __set__(self, instance: Model, value: str | None) -> None: ...

class ImageFieldFile(ImageFile, FieldFile[AnyStr]):
    field: ImageField
    def delete(self, save: bool = ...) -> None: ...

class ImageField(FileField):
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        width_field: str | None = ...,
        height_field: str | None = ...,
        **kwargs: Any,
    ) -> None: ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner: Any) -> ImageFileDescriptor: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner: Any) -> Any: ...
    # non-Model instances
    @overload
    def __get__(self: Self, instance: Any, owner: Any) -> Self: ...
    def update_dimension_fields(self, instance: Model, force: bool = ..., *args: Any, **kwargs: Any) -> None: ...
