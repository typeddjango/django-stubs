import decimal
import sys
import uuid
from datetime import date
from datetime import datetime as real_datetime
from datetime import time, timedelta
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from django.core import validators  # due to weird mypy.stubtest error
from django.core.checks import CheckMessage
from django.core.exceptions import FieldDoesNotExist as FieldDoesNotExist
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model
from django.db.models.expressions import Col, Combinable
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.query_utils import Q, RegisterLookupMixin
from django.forms import Field as FormField
from django.forms import Widget
from django.utils.datastructures import DictWrapper
from django.utils.functional import _Getter

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

class Empty: ...
class NOT_PROVIDED: ...

BLANK_CHOICE_DASH: List[Tuple[str, str]] = ...

_Choice = Tuple[Any, Any]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]
_ChoicesList = List[Union[_Choice, _ChoiceNamedGroup]]
_LimitChoicesTo = Union[Q, Dict[str, Any]]

class _ChoicesCallable(Protocol):
    def __call__(self) -> _FieldChoices: ...

_AllLimitChoicesTo = Union[_LimitChoicesTo, _ChoicesCallable]
_ErrorMessagesT = Dict[str, Any]

_T = TypeVar("_T", bound="Field")
# __set__ value type
_ST = TypeVar("_ST", contravariant=True)
# __get__ return type
_GT = TypeVar("_GT", covariant=True)

class Field(RegisterLookupMixin, Generic[_ST, _GT]):
    """
    Typing model fields.

    How does this work?
    Let's take a look at the self-contained example
    (it is way easier than our django implementation, but has the same concept).

    To understand this example you need:
    1. Be familiar with descriptors: https://docs.python.org/3/howto/descriptor.html
    2. Follow our explanation bellow

    Let's start with defining our fake model class and fake integer field.

    .. code:: python

        from typing import Generic, Union

        class Model(object):
            ...

        _SetType = Union[int, float]  # You can assign ints and floats
        _GetType = int  # access type is always `int`

        class IntField(object):
            def __get__(self, instance: Model, owner) -> _GetType:
                ...

            def __set__(self, instance, value: _SetType) -> None:
                ...

    Now, let's create our own example model,
    this would be something like ``User`` in your own apps:

    .. code:: python

        class Example(Model):
            count = IntField()

    And now, lets test that our reveal type works:

    .. code:: python

        example = Example()
        reveal_type(example.count)
        # Revealed type is "builtins.int"

        example.count = 1.5  # ok
        example.count = 'a'
        # Incompatible types in assignment
        # (expression has type "str", variable has type "Union[int, float]")

    Notice, that this is not magic. This is how descriptors work with ``mypy``.

    We also need ``_pyi_private_set_type`` attributes
    and friends to help inside our plugin.
    It is required to enhance parts like ``filter`` queries.
    """

    _pyi_private_set_type: Any
    _pyi_private_get_type: Any
    _pyi_lookup_exact_type: Any

    widget: Widget
    help_text: str
    attname: str
    auto_created: bool
    primary_key: bool
    remote_field: Optional[ForeignObjectRel]
    is_relation: bool
    related_model: Optional[Type[Model]]
    one_to_many: Optional[bool] = ...
    one_to_one: Optional[bool] = ...
    many_to_many: Optional[bool] = ...
    many_to_one: Optional[bool] = ...
    max_length: Optional[int]
    model: Type[Model]
    name: str
    verbose_name: str
    description: Union[str, _Getter[str]]
    blank: bool
    null: bool
    unique: bool
    editable: bool
    empty_strings_allowed: bool = ...
    choices: Optional[_ChoicesList] = ...
    db_column: Optional[str]
    column: str
    concrete: bool
    default: Any
    error_messages: _ErrorMessagesT
    empty_values: Sequence[Any] = ...
    creation_counter: int
    auto_creation_counter: int
    default_validators: Sequence[validators._ValidatorCallable]
    default_error_messages: Dict[str, str]
    hidden: bool
    system_check_removed_details: Optional[Any]
    system_check_deprecated_details: Optional[Any]
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
        rel: Optional[ForeignObjectRel] = ...,
        default: Any = ...,
        editable: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        auto_created: bool = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...
    def __set__(self, instance, value: _ST) -> None: ...
    # class access
    @overload
    def __get__(self: _T, instance: None, owner) -> _T: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner) -> _GT: ...
    # non-Model instances
    @overload
    def __get__(self: _T, instance, owner) -> _T: ...
    def deconstruct(self) -> Any: ...
    def set_attributes_from_name(self, name: str) -> None: ...
    def db_type_parameters(self, connection: BaseDatabaseWrapper) -> DictWrapper: ...
    def db_check(self, connection: BaseDatabaseWrapper) -> Optional[str]: ...
    def db_type(self, connection: BaseDatabaseWrapper) -> Optional[str]: ...
    def db_parameters(self, connection: BaseDatabaseWrapper) -> Dict[str, Optional[str]]: ...
    def pre_save(self, model_instance: Model, add: bool) -> Any: ...
    def get_prep_value(self, value: Any) -> Any: ...
    def get_db_prep_value(self, value: Any, connection: BaseDatabaseWrapper, prepared: bool = ...) -> Any: ...
    def get_db_prep_save(self, value: Any, connection: BaseDatabaseWrapper) -> Any: ...
    def get_internal_type(self) -> str: ...
    # TODO: plugin support
    def formfield(self, form_class: Optional[Any] = ..., choices_form_class: Optional[Any] = ..., **kwargs) -> Any: ...
    def save_form_data(self, instance: Model, data: Any) -> None: ...
    def contribute_to_class(self, cls: Type[Model], name: str, private_only: bool = ...) -> None: ...
    def to_python(self, value: Any) -> Any: ...
    @property
    def validators(self) -> List[validators._ValidatorCallable]: ...
    def run_validators(self, value: Any) -> None: ...
    def validate(self, value: Any, model_instance: Optional[Model]) -> None: ...
    def clean(self, value: Any, model_instance: Optional[Model]) -> Any: ...
    def get_choices(
        self,
        include_blank: bool = ...,
        blank_choice: _ChoicesList = ...,
        limit_choices_to: Optional[_LimitChoicesTo] = ...,
        ordering: Sequence[str] = ...,
    ) -> _ChoicesList: ...
    def has_default(self) -> bool: ...
    def get_default(self) -> Any: ...
    def check(self, **kwargs: Any) -> List[CheckMessage]: ...
    def get_col(self, alias: str, output_field: Optional[Field] = ...) -> Col: ...
    @property
    def cached_col(self) -> Col: ...
    def value_from_object(self, obj: Model) -> _GT: ...
    def get_attname(self) -> str: ...
    def value_to_string(self, obj: Model) -> str: ...

class IntegerField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[float, int, str, Combinable]
    _pyi_private_get_type: int
    _pyi_lookup_exact_type: Union[str, int]

class PositiveIntegerRelDbTypeMixin:
    def rel_db_type(self, connection: BaseDatabaseWrapper) -> str: ...

class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField[_ST, _GT]): ...
class PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, SmallIntegerField[_ST, _GT]): ...
class PositiveBigIntegerField(PositiveIntegerRelDbTypeMixin, BigIntegerField[_ST, _GT]): ...
class SmallIntegerField(IntegerField[_ST, _GT]): ...
class BigIntegerField(IntegerField[_ST, _GT]): ...

class FloatField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[float, int, str, Combinable]
    _pyi_private_get_type: float
    _pyi_lookup_exact_type: float

class DecimalField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, float, decimal.Decimal, Combinable]
    _pyi_private_get_type: decimal.Decimal
    _pyi_lookup_exact_type: Union[str, decimal.Decimal]
    # attributes
    max_digits: int = ...
    decimal_places: int = ...
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        max_digits: Optional[int] = ...,
        decimal_places: Optional[int] = ...,
        *,
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...

class CharField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, int, Combinable]
    _pyi_private_get_type: str
    # objects are converted to string before comparison
    _pyi_lookup_exact_type: Any
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        *,
        db_collation: Optional[str] = ...,
    ): ...

class CommaSeparatedIntegerField(CharField[_ST, _GT]): ...

class SlugField(CharField[_ST, _GT]):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
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
        *,
        max_length: Optional[int] = ...,
        db_index: bool = ...,
        allow_unicode: bool = ...,
    ): ...

class EmailField(CharField[_ST, _GT]): ...

class URLField(CharField[_ST, _GT]):
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        *,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        rel: Optional[ForeignObjectRel] = ...,
        default: Any = ...,
        editable: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        auto_created: bool = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...

class TextField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, Combinable]
    _pyi_private_get_type: str
    # objects are converted to string before comparison
    _pyi_lookup_exact_type: Any
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
        *,
        db_collation: Optional[str] = ...,
    ): ...

class BooleanField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[bool, Combinable]
    _pyi_private_get_type: bool
    _pyi_lookup_exact_type: bool

class NullBooleanField(BooleanField[_ST, _GT]):
    _pyi_private_set_type: Optional[Union[bool, Combinable]]  # type: ignore
    _pyi_private_get_type: Optional[bool]  # type: ignore
    _pyi_lookup_exact_type: Optional[bool]  # type: ignore

class IPAddressField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, Combinable]
    _pyi_private_get_type: str

class GenericIPAddressField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, int, Callable[..., Any], Combinable]
    _pyi_private_get_type: str

    default_error_messages: Dict[str, str] = ...
    unpack_ipv4: bool = ...
    protocol: str = ...
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ) -> None: ...

class DateTimeCheckMixin: ...

class DateField(DateTimeCheckMixin, Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, date, Combinable]
    _pyi_private_get_type: date
    _pyi_lookup_exact_type: Union[str, date]
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        auto_now: bool = ...,
        auto_now_add: bool = ...,
        *,
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...

class TimeField(DateTimeCheckMixin, Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, time, real_datetime, Combinable]
    _pyi_private_get_type: time
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        auto_now: bool = ...,
        auto_now_add: bool = ...,
        *,
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...

class DateTimeField(DateField[_ST, _GT]):
    _pyi_private_set_type: Union[str, real_datetime, date, Combinable]
    _pyi_private_get_type: real_datetime
    _pyi_lookup_exact_type: Union[str, real_datetime]

class UUIDField(Field[_ST, _GT]):
    _pyi_private_set_type: Union[str, uuid.UUID]
    _pyi_private_get_type: uuid.UUID
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        *,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        rel: Optional[ForeignObjectRel] = ...,
        default: Any = ...,
        editable: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        auto_created: bool = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...

class FilePathField(Field[_ST, _GT]):
    path: Any = ...
    match: Optional[str] = ...
    recursive: bool = ...
    allow_files: bool = ...
    allow_folders: bool = ...
    def __init__(
        self,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        path: Union[str, Callable[..., str]] = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        *,
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesT] = ...,
    ): ...

class BinaryField(Field[_ST, _GT]):
    _pyi_private_get_type: Union[bytes, memoryview]

class DurationField(Field[_ST, _GT]):
    _pyi_private_get_type: timedelta

class AutoFieldMixin:
    db_returning: bool = ...

class AutoFieldMeta(type): ...

class AutoField(AutoFieldMixin, IntegerField[_ST, _GT], metaclass=AutoFieldMeta):
    _pyi_private_set_type: Union[Combinable, int, str]
    _pyi_private_get_type: int
    _pyi_lookup_exact_type: Union[str, int]

class BigAutoField(AutoFieldMixin, BigIntegerField[_ST, _GT]): ...
class SmallAutoField(AutoFieldMixin, SmallIntegerField[_ST, _GT]): ...
