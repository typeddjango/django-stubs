from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.core.checks.messages import Error
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage, Storage
from django.db.models.base import Model
from django.db.models.fields import Field
from django.forms.fields import FileField, ImageField


class FieldFile(File):
    instance: django.db.models.base.Model = ...
    field: django.db.models.fields.files.FileField = ...
    storage: Union[
        django.core.files.storage.DefaultStorage,
        django.core.files.storage.FileSystemStorage,
    ] = ...
    def __init__(
        self, instance: Model, field: FileField, name: Optional[str]
    ) -> None: ...
    def __eq__(
        self,
        other: Optional[
            Union[Dict[Any, Any], List[Any], Tuple, FieldFile, str]
        ],
    ) -> bool: ...
    def __hash__(self): ...
    file: Any = ...
    @property
    def path(self) -> str: ...
    @property
    def url(self) -> str: ...
    @property
    def size(self) -> int: ...
    def open(self, mode: str = ...) -> FieldFile: ...
    name: Optional[str] = ...
    def save(self, name: str, content: File, save: bool = ...) -> None: ...
    def delete(self, save: bool = ...) -> None: ...
    @property
    def closed(self) -> bool: ...
    def close(self) -> None: ...

class FileDescriptor:
    field: django.db.models.fields.files.FileField = ...
    def __init__(self, field: FileField) -> None: ...
    def __get__(
        self, instance: Optional[Model], cls: Type[Model] = ...
    ) -> Union[FieldFile, FileDescriptor]: ...
    def __set__(
        self, instance: Model, value: Optional[Union[File, str]]
    ) -> None: ...

class FileField(Field):
    attr_class: Any = ...
    descriptor_class: Any = ...
    description: Any = ...
    storage: Any = ...
    upload_to: Any = ...
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: None = ...,
        upload_to: Union[Callable, str] = ...,
        storage: Optional[Storage] = ...,
        **kwargs: Any
    ) -> None: ...
    def check(self, **kwargs: Any) -> List[Error]: ...
    def deconstruct(
        self
    ) -> Union[
        Tuple[
            None,
            str,
            List[Any],
            Union[
                Dict[str, Union[Callable, FileSystemStorage]],
                Dict[str, Union[partial, int]],
            ],
        ],
        Tuple[
            str,
            List[Any],
            Union[
                Dict[str, Union[Callable, FileSystemStorage, int]],
                Dict[str, Union[FileSystemStorage, int, str]],
            ],
            Union[
                Dict[str, Union[Callable, FileSystemStorage, int]],
                Dict[str, Union[FileSystemStorage, int, str]],
            ],
        ],
        Tuple[
            str,
            str,
            List[Any],
            Union[
                Dict[str, Union[Callable, bool, FileSystemStorage]],
                Dict[str, str],
            ],
        ],
    ]: ...
    def get_internal_type(self) -> str: ...
    def get_prep_value(self, value: Union[FieldFile, str]) -> str: ...
    def pre_save(self, model_instance: Model, add: bool) -> FieldFile: ...
    def contribute_to_class(
        self, cls: Type[Model], name: str, **kwargs: Any
    ) -> None: ...
    def generate_filename(
        self, instance: Optional[Model], filename: str
    ) -> str: ...
    def save_form_data(
        self, instance: Model, data: Optional[Union[bool, File, str]]
    ) -> None: ...
    def formfield(self, **kwargs: Any) -> FileField: ...

class ImageFileDescriptor(FileDescriptor):
    field: django.db.models.fields.files.ImageField
    def __set__(self, instance: Model, value: Optional[str]) -> None: ...

class ImageFieldFile(ImageFile, FieldFile):
    field: django.db.models.fields.files.ImageField
    instance: django.db.models.base.Model
    name: Optional[str]
    storage: django.core.files.storage.DefaultStorage
    def delete(self, save: bool = ...) -> None: ...

class ImageField(FileField):
    attr_class: Any = ...
    descriptor_class: Any = ...
    description: Any = ...
    def __init__(
        self,
        verbose_name: None = ...,
        name: None = ...,
        width_field: Optional[str] = ...,
        height_field: Optional[str] = ...,
        **kwargs: Any
    ) -> None: ...
    def check(self, **kwargs: Any) -> List[Any]: ...
    def deconstruct(
        self
    ) -> Union[
        Tuple[
            str,
            List[Any],
            Dict[str, Union[Callable, bool, FileSystemStorage, str]],
            Dict[str, Union[Callable, bool, FileSystemStorage, str]],
        ],
        Tuple[
            str, str, List[Any], Dict[str, Union[Callable, FileSystemStorage]]
        ],
    ]: ...
    def contribute_to_class(
        self, cls: Type[Model], name: str, **kwargs: Any
    ) -> None: ...
    def update_dimension_fields(
        self, instance: Model, force: bool = ..., *args: Any, **kwargs: Any
    ) -> None: ...
    def formfield(self, **kwargs: Any) -> ImageField: ...
