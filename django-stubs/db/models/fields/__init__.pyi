from typing import Any, Optional, Tuple, Iterable, Callable, Dict, Union, Type
import decimal

from django.db.models import Model
from django.db.models.query_utils import RegisterLookupMixin

from django.db.models.expressions import F, Combinable
from django.forms import Widget, Field as FormField
from .mixins import NOT_PROVIDED as NOT_PROVIDED

_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]

_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]

class Field(RegisterLookupMixin):
    widget: Widget
    help_text: str
    db_table: str
    remote_field: Field
    model: Type[Model]
    name: str
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
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
    def formfield(self, **kwargs) -> FormField: ...
    def contribute_to_class(self, cls: Type[Model], name: str, private_only: bool = ...) -> None: ...

class IntegerField(Field):
    def __set__(self, instance, value: Union[int, F]) -> None: ...
    def __get__(self, instance, owner) -> int: ...

class PositiveIntegerRelDbTypeMixin:
    def rel_db_type(self, connection: Any): ...

class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField): ...
class PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField): ...
class SmallIntegerField(IntegerField): ...
class BigIntegerField(IntegerField): ...
class FloatField(Field): ...

class DecimalField(Field):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
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
    def __get__(self, instance, owner) -> decimal.Decimal: ...

class AutoField(Field):
    def __get__(self, instance, owner) -> int: ...

class CharField(Field):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
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
        verbose_name: Optional[str] = ...,
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

class FileField(Field): ...
class IPAddressField(Field): ...

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

class DateTimeCheckMixin: ...

class DateField(DateTimeCheckMixin, Field):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
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

class TimeField(DateTimeCheckMixin, Field):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
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

class DateTimeField(DateField): ...
class UUIDField(Field): ...

class FilePathField(Field):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
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
class DurationField(Field): ...
class BigAutoField(AutoField): ...
