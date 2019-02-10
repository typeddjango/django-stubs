import uuid
from datetime import date, time, datetime, timedelta
from typing import Any, Optional, Tuple, Iterable, Callable, Dict, Union, Type, TypeVar
import decimal

from typing_extensions import Literal

from django.db.models import Model
from django.db.models.query_utils import RegisterLookupMixin

from django.db.models.expressions import F, Combinable
from django.core.exceptions import FieldDoesNotExist as FieldDoesNotExist
from django.forms import Widget, Field as FormField
from .mixins import NOT_PROVIDED as NOT_PROVIDED

_Choice = Tuple[Any, Any]
_ChoiceNamedGroup = Union[Tuple[str, Iterable[_Choice]], Tuple[str, Any]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]

_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]

class Field(RegisterLookupMixin):
    widget: Widget
    help_text: str
    db_table: str
    remote_field: Field
    max_length: Optional[int]
    model: Type[Model]
    name: str
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
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
    def __get__(self, instance, owner) -> Any: ...
    def deconstruct(self) -> Any: ...
    def set_attributes_from_name(self, name: str) -> None: ...
    def db_type(self, connection: Any) -> str: ...
    def db_parameters(self, connection: Any) -> Dict[str, str]: ...
    def get_prep_value(self, value: Any) -> Any: ...
    def get_internal_type(self) -> str: ...
    def formfield(self, **kwargs) -> FormField: ...
    def contribute_to_class(self, cls: Type[Model], name: str, private_only: bool = ...) -> None: ...
    def to_python(self, value: Any) -> Any: ...

class IntegerField(Field):
    def __set__(self, instance, value: Union[int, Combinable, Literal['']]) -> None: ...
    def __get__(self, instance, owner) -> int: ...

class PositiveIntegerRelDbTypeMixin:
    def rel_db_type(self, connection: Any): ...

class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField): ...
class PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField): ...
class SmallIntegerField(IntegerField): ...
class BigIntegerField(IntegerField): ...

class FloatField(Field):
    def __set__(self, instance, value: Union[float, int, Combinable]) -> float: ...
    def __get__(self, instance, owner) -> float: ...

class DecimalField(Field):
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        max_digits: Optional[int] = ...,
        decimal_places: Optional[int] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...
    def __set__(self, instance, value: Union[str, Combinable]) -> decimal.Decimal: ...
    def __get__(self, instance, owner) -> decimal.Decimal: ...

class AutoField(Field):
    def __get__(self, instance, owner) -> int: ...

class CharField(Field):
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
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
    def __set__(self, instance, value: Union[str, Combinable]) -> None: ...
    def __get__(self, instance, owner) -> str: ...

class SlugField(CharField):
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        allow_unicode: bool = ...,
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

class EmailField(CharField): ...
class URLField(CharField): ...

class TextField(Field):
    def __set__(self, instance, value: str) -> None: ...
    def __get__(self, instance, owner) -> str: ...

class BooleanField(Field):
    def __set__(self, instance, value: bool) -> None: ...
    def __get__(self, instance, owner) -> bool: ...

class NullBooleanField(Field):
    def __set__(self, instance, value: Optional[bool]) -> None: ...
    def __get__(self, instance, owner) -> Optional[bool]: ...

class IPAddressField(Field):
    def __get__(self, instance, owner) -> str: ...

class GenericIPAddressField(Field):
    default_error_messages: Any = ...
    unpack_ipv4: Any = ...
    protocol: Any = ...
    def __init__(
        self,
        verbose_name: Optional[Any] = ...,
        name: Optional[Any] = ...,
        protocol: str = ...,
        unpack_ipv4: bool = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    def __get__(self, instance, owner) -> str: ...

class DateTimeCheckMixin: ...

class DateField(DateTimeCheckMixin, Field):
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        auto_now: bool = ...,
        auto_now_add: bool = ...,
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
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...
    def __set__(self, instance, value: Union[str, date, Combinable]) -> None: ...
    def __get__(self, instance, owner) -> date: ...

class TimeField(DateTimeCheckMixin, Field):
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        auto_now: bool = ...,
        auto_now_add: bool = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...
    def __set__(self, instance, value: Union[str, time, datetime, Combinable]) -> None: ...
    def __get__(self, instance, owner) -> time: ...

class DateTimeField(DateField):
    def __set__(self, instance, value: Union[str, date, datetime, Combinable]) -> None: ...
    def __get__(self, instance, owner) -> datetime: ...

class UUIDField(Field):
    def __set__(self, instance, value: Any) -> None: ...
    def __get__(self, instance, owner) -> uuid.UUID: ...

class FilePathField(Field):
    path: str = ...
    match: Optional[Any] = ...
    recursive: bool = ...
    allow_files: bool = ...
    allow_folders: bool = ...
    def __init__(
        self,
        verbose_name: Optional[Union[str, bytes]] = ...,
        name: Optional[str] = ...,
        path: str = ...,
        match: Optional[Any] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        primary_key: bool = ...,
        max_length: int = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ): ...

class BinaryField(Field): ...

class DurationField(Field):
    def __get__(self, instance, owner) -> timedelta: ...

class BigAutoField(AutoField): ...
class CommaSeparatedIntegerField(CharField): ...
