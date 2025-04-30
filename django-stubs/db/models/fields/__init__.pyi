import decimal
import uuid
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import date, time, timedelta
from datetime import datetime as real_datetime
from typing import Any, ClassVar, Generic, Literal, Protocol, TypeAlias, overload, type_check_only

from django import forms
from django.core import validators  # due to weird mypy.stubtest error
from django.core.checks import CheckMessage
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model
from django.db.models.expressions import Col, Combinable, Expression, Func
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.query_utils import Q, RegisterLookupMixin
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType, _ParamsT
from django.forms import Widget
from django.utils.choices import BlankChoiceIterator, _Choice, _ChoiceNamedGroup, _ChoicesCallable, _ChoicesInput
from django.utils.datastructures import DictWrapper
from django.utils.functional import _Getter, _StrOrPromise, cached_property
from typing_extensions import Self, TypeVar

class Empty: ...
class NOT_PROVIDED: ...

BLANK_CHOICE_DASH: list[tuple[str, str]]

_ChoicesList: TypeAlias = Sequence[_Choice] | Sequence[_ChoiceNamedGroup]
_LimitChoicesTo: TypeAlias = Q | dict[str, Any]
_LimitChoicesToCallable: TypeAlias = Callable[[], _LimitChoicesTo]

_F = TypeVar("_F", bound=Field, covariant=True)

@type_check_only
class _FieldDescriptor(Protocol[_F]):
    """
    Accessing fields of a model class (not instance) returns an object conforming to this protocol.
    Depending on field type this could be DeferredAttribute, ForwardManyToOneDescriptor, FileDescriptor, etc.
    """

    @property
    def field(self) -> _F: ...

_AllLimitChoicesTo: TypeAlias = _LimitChoicesTo | _LimitChoicesToCallable | _ChoicesCallable  # noqa: PYI047
_ErrorMessagesMapping: TypeAlias = Mapping[str, _StrOrPromise]
_ErrorMessagesDict: TypeAlias = dict[str, _StrOrPromise]

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
    2. Follow our explanation below

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
    help_text: _StrOrPromise
    attname: str
    auto_created: bool
    primary_key: bool
    remote_field: ForeignObjectRel | None
    is_relation: bool
    related_model: type[Model] | Literal["self"] | None
    generated: ClassVar[bool]
    one_to_many: bool | None
    one_to_one: bool | None
    many_to_many: bool | None
    many_to_one: bool | None
    max_length: int | None
    model: type[Model]
    name: str
    verbose_name: _StrOrPromise
    description: str | _Getter[str]
    blank: bool
    null: bool
    unique: bool
    editable: bool
    empty_strings_allowed: bool
    choices: _ChoicesList | None
    db_column: str | None
    db_comment: str | None
    db_default: type[NOT_PROVIDED] | Expression
    column: str
    concrete: bool
    default: Any
    error_messages: _ErrorMessagesDict
    empty_values: Sequence[Any]
    creation_counter: int
    auto_creation_counter: int
    default_validators: Sequence[validators._ValidatorCallable]
    default_error_messages: ClassVar[_ErrorMessagesDict]
    hidden: bool
    system_check_removed_details: Any | None
    system_check_deprecated_details: Any | None
    non_db_attrs: tuple[str, ...]
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        unique: bool = False,
        blank: bool = False,
        null: bool = False,
        db_index: bool = False,
        rel: ForeignObjectRel | None = None,
        default: Any = ...,
        editable: bool = True,
        serialize: bool = True,
        unique_for_date: str | None = None,
        unique_for_month: str | None = None,
        unique_for_year: str | None = None,
        choices: _ChoicesInput | None = None,
        help_text: _StrOrPromise = "",
        db_column: str | None = None,
        db_tablespace: str | None = None,
        auto_created: bool = False,
        validators: Iterable[validators._ValidatorCallable] = (),
        error_messages: _ErrorMessagesMapping | None = None,
        db_comment: str | None = None,
        db_default: type[NOT_PROVIDED] | Expression | _ST = ...,  # pyright: ignore[reportInvalidTypeVarUse]
    ) -> None: ...
    def __set__(self, instance: Any, value: _ST) -> None: ...
    # class access
    @overload
    def __get__(self, instance: None, owner: Any) -> _FieldDescriptor[Self]: ...
    # Model instance access
    @overload
    def __get__(self, instance: Model, owner: Any) -> _GT: ...
    # non-Model instances
    @overload
    def __get__(self, instance: Any, owner: Any) -> Self: ...
    def select_format(self, compiler: SQLCompiler, sql: str, params: _ParamsT) -> _AsSqlType: ...
    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]: ...
    def set_attributes_from_name(self, name: str) -> None: ...
    def db_type_parameters(self, connection: BaseDatabaseWrapper) -> DictWrapper: ...
    def db_check(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def db_type(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def db_parameters(self, connection: BaseDatabaseWrapper) -> dict[str, str | None]: ...
    def pre_save(self, model_instance: Model, add: bool) -> Any: ...
    def get_prep_value(self, value: Any) -> Any: ...
    def get_db_prep_value(self, value: Any, connection: BaseDatabaseWrapper, prepared: bool = False) -> Any: ...
    def get_db_prep_save(self, value: Any, connection: BaseDatabaseWrapper) -> Any: ...
    def get_internal_type(self) -> str: ...
    # TODO: plugin support
    def formfield(
        self,
        form_class: type[forms.Field] | None = None,
        choices_form_class: type[forms.ChoiceField] | None = None,
        **kwargs: Any,
    ) -> forms.Field | None: ...
    def save_form_data(self, instance: Model, data: Any) -> None: ...
    def contribute_to_class(self, cls: type[Model], name: str, private_only: bool = False) -> None: ...
    def to_python(self, value: Any) -> Any: ...
    @cached_property
    def validators(self) -> list[validators._ValidatorCallable]: ...
    def run_validators(self, value: Any) -> None: ...
    def validate(self, value: Any, model_instance: Model | None) -> None: ...
    def clean(self, value: Any, model_instance: Model | None) -> Any: ...
    def get_choices(
        self,
        include_blank: bool = True,
        blank_choice: _ChoicesList = ...,
        limit_choices_to: _LimitChoicesTo | None = None,
        ordering: Sequence[str] = (),
    ) -> BlankChoiceIterator | _ChoicesList: ...
    @property
    def flatchoices(self) -> list[_Choice]: ...
    def has_default(self) -> bool: ...
    def get_default(self) -> Any: ...
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    def get_col(self, alias: str, output_field: Field[Any, Any] | None = None) -> Col: ...
    @cached_property
    def cached_col(self) -> Col: ...
    def value_from_object(self, obj: Model) -> _GT: ...
    def get_attname(self) -> str: ...
    def get_attname_column(self) -> tuple[str, str]: ...
    def value_to_string(self, obj: Model) -> str: ...
    def slice_expression(self, expression: Expression, start: int, length: int | None) -> Func: ...

_ST_IntegerField = TypeVar("_ST_IntegerField", default=float | int | str | Combinable)
_GT_IntegerField = TypeVar("_GT_IntegerField", default=int)

class IntegerField(Field[_ST_IntegerField, _GT_IntegerField]):
    _pyi_private_set_type: float | int | str | Combinable
    _pyi_private_get_type: int
    _pyi_lookup_exact_type: str | int

class PositiveIntegerRelDbTypeMixin:
    def rel_db_type(self, connection: BaseDatabaseWrapper) -> str: ...

class SmallIntegerField(IntegerField[_ST_IntegerField, _GT_IntegerField]): ...

class BigIntegerField(IntegerField[_ST_IntegerField, _GT_IntegerField]):
    MAX_BIGINT: ClassVar[int]

class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField[_ST_IntegerField, _GT_IntegerField]): ...
class PositiveSmallIntegerField(
    PositiveIntegerRelDbTypeMixin, SmallIntegerField[_ST_IntegerField, _GT_IntegerField]
): ...
class PositiveBigIntegerField(PositiveIntegerRelDbTypeMixin, BigIntegerField[_ST_IntegerField, _GT_IntegerField]): ...

_ST_FloatField = TypeVar("_ST_FloatField", default=float | int | str | Combinable)
_GT_FloatField = TypeVar("_GT_FloatField", default=float)

class FloatField(Field[_ST_FloatField, _GT_FloatField]):
    _pyi_private_set_type: float | int | str | Combinable
    _pyi_private_get_type: float
    _pyi_lookup_exact_type: float

_ST_DecimalField = TypeVar("_ST_DecimalField", default=str | float | decimal.Decimal | Combinable)
_GT_DecimalField = TypeVar("_GT_DecimalField", default=decimal.Decimal)

class DecimalField(Field[_ST_DecimalField, _GT_DecimalField]):
    _pyi_private_set_type: str | float | decimal.Decimal | Combinable
    _pyi_private_get_type: decimal.Decimal
    _pyi_lookup_exact_type: str | decimal.Decimal
    # attributes
    max_digits: int
    decimal_places: int
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        max_digits: int | None = None,
        decimal_places: int | None = None,
        *,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_DecimalField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

_ST_CharField = TypeVar("_ST_CharField", default=str | int | Combinable)
_GT_CharField = TypeVar("_GT_CharField", default=str)

class CharField(Field[_ST_CharField, _GT_CharField]):
    _pyi_private_set_type: str | int | Combinable
    _pyi_private_get_type: str
    # objects are converted to string before comparison
    _pyi_lookup_exact_type: Any
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_CharField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        *,
        db_collation: str | None = None,
    ) -> None: ...

class CommaSeparatedIntegerField(CharField[_ST_CharField, _GT_CharField]): ...

class SlugField(CharField[_ST_CharField, _GT_CharField]):
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_CharField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        *,
        max_length: int | None = 50,
        db_index: bool = True,
        allow_unicode: bool = False,
    ) -> None: ...

_ST_EmailField = TypeVar("_ST_EmailField", default=str | Combinable)
_GT_EmailField = TypeVar("_GT_EmailField", default=str)

class EmailField(CharField[_ST_EmailField, _GT_EmailField]):
    _pyi_private_set_type: str | Combinable

class URLField(CharField[_ST_CharField, _GT_CharField]):
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        rel: ForeignObjectRel | None = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_CharField = ...,
        editable: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        auto_created: bool = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

_ST_TextField = TypeVar("_ST_TextField", default=str | Combinable)
_GT_TextField = TypeVar("_GT_TextField", default=str)

class TextField(Field[_ST_TextField, _GT_TextField]):
    _pyi_private_set_type: str | Combinable
    _pyi_private_get_type: str
    # objects are converted to string before comparison
    _pyi_lookup_exact_type: Any
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_TextField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        *,
        db_collation: str | None = None,
    ) -> None: ...

_ST_BooleanField = TypeVar("_ST_BooleanField", default=bool | Combinable)
_GT_BooleanField = TypeVar("_GT_BooleanField", default=bool)

class BooleanField(Field[_ST_BooleanField, _GT_BooleanField]):
    _pyi_private_set_type: bool | Combinable
    _pyi_private_get_type: bool
    _pyi_lookup_exact_type: bool

class NullBooleanField(BooleanField[_ST_BooleanField, _GT_BooleanField]):
    _pyi_private_set_type: bool | Combinable | None  # type: ignore[assignment]
    _pyi_private_get_type: bool | None  # type: ignore[assignment]
    _pyi_lookup_exact_type: bool | None  # type: ignore[assignment]

_ST_IPAddressField = TypeVar("_ST_IPAddressField", default=str | Combinable)
_GT_IPAddressField = TypeVar("_GT_IPAddressField", default=str)

class IPAddressField(Field[_ST_IPAddressField, _GT_IPAddressField]):
    _pyi_private_set_type: str | Combinable
    _pyi_private_get_type: str

_ST_GenericIPAddressField = TypeVar("_ST_GenericIPAddressField", default=str | int | Callable[..., Any] | Combinable)
_GT_GenericIPAddressField = TypeVar("_GT_GenericIPAddressField", default=str)

class GenericIPAddressField(Field[_ST_GenericIPAddressField, _GT_GenericIPAddressField]):
    _pyi_private_set_type: str | int | Callable[..., Any] | Combinable
    _pyi_private_get_type: str

    default_error_messages: ClassVar[_ErrorMessagesDict]
    unpack_ipv4: bool
    protocol: str
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: Any | None = None,
        protocol: str = "both",
        unpack_ipv4: bool = False,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_GenericIPAddressField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

class DateTimeCheckMixin: ...

_ST_DateField = TypeVar("_ST_DateField", default=str | date | Combinable)
_GT_DateField = TypeVar("_GT_DateField", default=date)

class DateField(DateTimeCheckMixin, Field[_ST_DateField, _GT_DateField]):
    _pyi_private_set_type: str | date | Combinable
    _pyi_private_get_type: date
    _pyi_lookup_exact_type: str | date
    auto_now: bool
    auto_now_add: bool
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        auto_now: bool = False,
        auto_now_add: bool = False,
        *,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_DateField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

_ST_TimeField = TypeVar("_ST_TimeField", default=str | time | real_datetime | Combinable)
_GT_TimeField = TypeVar("_GT_TimeField", default=time)

class TimeField(DateTimeCheckMixin, Field[_ST_TimeField, _GT_TimeField]):
    _pyi_private_set_type: str | time | real_datetime | Combinable
    _pyi_private_get_type: time
    auto_now: bool
    auto_now_add: bool
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        auto_now: bool = False,
        auto_now_add: bool = False,
        *,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_TimeField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

_ST_DateTimeField = TypeVar("_ST_DateTimeField", default=str | real_datetime | date | Combinable)
_GT_DateTimeField = TypeVar("_GT_DateTimeField", default=real_datetime)

class DateTimeField(DateField[_ST_DateTimeField, _GT_DateTimeField]):
    _pyi_private_set_type: str | real_datetime | date | Combinable
    _pyi_private_get_type: real_datetime
    _pyi_lookup_exact_type: str | real_datetime

_ST_UUIDField = TypeVar("_ST_UUIDField", default=str | uuid.UUID)
_GT_UUIDField = TypeVar("_GT_UUIDField", default=uuid.UUID)

class UUIDField(Field[_ST_UUIDField, _GT_UUIDField]):
    _pyi_private_set_type: str | uuid.UUID
    _pyi_private_get_type: uuid.UUID
    _pyi_lookup_exact_type: uuid.UUID | str
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        *,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        rel: ForeignObjectRel | None = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_UUIDField = ...,
        editable: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        auto_created: bool = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

_ST_FileField = TypeVar("_ST_FileField", default=str | bytes | memoryview)
_GT_FileField = TypeVar("_GT_FileField", default=str)

class FilePathField(Field[_ST_FileField, _GT_FileField]):
    path: Any
    match: str | None
    recursive: bool
    allow_files: bool
    allow_folders: bool
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        path: str | Callable[..., str] = "",
        match: str | None = None,
        recursive: bool = False,
        allow_files: bool = True,
        allow_folders: bool = False,
        *,
        primary_key: bool = ...,
        max_length: int = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_FileField = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...

_ST_BinaryField = TypeVar("_ST_BinaryField", default=bytes | memoryview)
_GT_BinaryField = TypeVar("_GT_BinaryField", default=bytes | memoryview)

class BinaryField(Field[_ST_BinaryField, _GT_BinaryField]):
    _pyi_private_get_type: bytes | memoryview

_ST_DurationField = TypeVar("_ST_DurationField", default=timedelta)
_GT_DurationField = TypeVar("_GT_DurationField", default=timedelta)

class DurationField(Field[_ST_DurationField, _GT_DurationField]):
    _pyi_private_get_type: timedelta

class AutoFieldMixin:
    db_returning: bool
    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]: ...

class AutoFieldMeta(type): ...

_ST_AutoField = TypeVar("_ST_AutoField", default=Combinable | int | str | None)
_GT_AutoField = TypeVar("_GT_AutoField", default=int)

class AutoField(AutoFieldMixin, IntegerField[_ST_AutoField, _GT_AutoField], metaclass=AutoFieldMeta):
    _pyi_private_set_type: Combinable | int | str

class BigAutoField(AutoFieldMixin, BigIntegerField[_ST_AutoField, _GT_AutoField]): ...
class SmallAutoField(AutoFieldMixin, SmallIntegerField[_ST_AutoField, _GT_AutoField]): ...

__all__ = [
    "AutoField",
    "BLANK_CHOICE_DASH",
    "BigAutoField",
    "BigIntegerField",
    "BinaryField",
    "BooleanField",
    "CharField",
    "CommaSeparatedIntegerField",
    "DateField",
    "DateTimeField",
    "DecimalField",
    "DurationField",
    "EmailField",
    "Empty",
    "Field",
    "FilePathField",
    "FloatField",
    "GenericIPAddressField",
    "IPAddressField",
    "IntegerField",
    "NOT_PROVIDED",
    "NullBooleanField",
    "PositiveBigIntegerField",
    "PositiveIntegerField",
    "PositiveSmallIntegerField",
    "SlugField",
    "SmallAutoField",
    "SmallIntegerField",
    "TextField",
    "TimeField",
    "URLField",
    "UUIDField",
]
