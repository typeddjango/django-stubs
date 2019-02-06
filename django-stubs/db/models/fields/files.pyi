from typing import Any, Callable, List, Optional, Type, Union, Tuple, Iterable

from django.core.checks.messages import Error
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage, Storage
from django.db.models.base import Model

from django.db.models.fields import Field, _FieldChoices, _ValidatorCallable, _ErrorMessagesToOverride
from django.forms import fields as form_fields

BLANK_CHOICE_DASH: List[Tuple[str, str]] = ...

class FieldFile(File):
    instance: Model = ...
    field: FileField = ...
    storage: FileSystemStorage = ...
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

class FileDescriptor:
    field: FileField = ...
    def __init__(self, field: FileField) -> None: ...
    def __set__(self, instance: Model, value: Optional[Any]) -> None: ...
    def __get__(self, instance: Optional[Model], cls: Type[Model] = ...) -> Union[FieldFile, FileDescriptor]: ...

class FileField(Field):
    storage: Any = ...
    upload_to: Union[str, Callable] = ...
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        upload_to: Union[str, Callable] = ...,
        storage: Optional[Storage] = ...,
        primary_key: bool = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...
    def generate_filename(self, instance: Optional[Model], filename: str) -> str: ...

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
        **kwargs: Any
    ) -> None: ...
    def update_dimension_fields(self, instance: Model, force: bool = ..., *args: Any, **kwargs: Any) -> None: ...
