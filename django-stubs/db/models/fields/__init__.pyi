import decimal
import uuid
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import date, time, timedelta
from datetime import datetime as real_datetime
from typing import Any, ClassVar, Generic, Literal, Protocol, TypeAlias, overload, type_check_only

from django import forms
from django.core.checks import CheckMessage
from django.core.validators import _ValidatorCallable
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model
from django.db.models.expressions import Col, Combinable, Expression, Func
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.query import _OrderByFieldName
from django.db.models.query_utils import Q, RegisterLookupMixin
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType, _ParamsT
from django.utils.choices import BlankChoiceIterator, _Choice, _ChoiceNamedGroup, _ChoicesCallable, _ChoicesInput
from django.utils.datastructures import DictWrapper
from django.utils.functional import _Getter, _StrOrPromise, cached_property
from typing_extensions import Self, TypeVar, override

class Empty: ...
class NOT_PROVIDED: ...

BLANK_CHOICE_DASH: list[tuple[str, str]]

_ChoicesList: TypeAlias = Sequence[_Choice] | Sequence[_ChoiceNamedGroup]
_LimitChoicesTo: TypeAlias = Q | dict[str, Any]
_LimitChoicesToCallable: TypeAlias = Callable[[], _LimitChoicesTo]

_F = TypeVar("_F", bound=Field[Any, Any, Any], covariant=True)

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
_ST = TypeVar("_ST", contravariant=True, default=Any)
# __get__ return type
_GT = TypeVar("_GT", covariant=True, default=Any)
# null flag type
_NT = TypeVar("_NT", Literal[True], Literal[False], default=Literal[False])

class Field(RegisterLookupMixin, Generic[_ST, _GT, _NT]):
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

        from typing import Generic

        class Model(object):
            ...

        _SetType = int | float  # You can assign ints and floats
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
        # Revealed type is "int"

        example.count = 1.5  # ok
        example.count = 'a'
        # Incompatible types in assignment
        # (expression has type "str", variable has type "int | float")

    Notice, that this is not magic. This is how descriptors work with ``mypy``.

    We also need ``_pyi_lookup_exact_type`` to help inside our plugin.
    It is required to enhance parts like ``filter`` queries.
    """

    _pyi_lookup_exact_type: Any

    help_text: _StrOrPromise
    attname: str
    auto_created: bool
    primary_key: bool
    remote_field: ForeignObjectRel | None
    is_relation: bool
    related_model: type[Model] | None
    generated: ClassVar[bool]
    one_to_many: bool | None
    one_to_one: bool | None
    many_to_many: bool | None
    many_to_one: bool | None
    max_length: int | None
    model: type[Model]
    name: str
    verbose_name: _StrOrPromise
    description: _StrOrPromise | _Getter[_StrOrPromise]
    blank: bool
    null: bool
    editable: bool
    empty_strings_allowed: bool
    choices: _ChoicesList | None
    db_column: str | None
    db_comment: str | None
    db_default: type[NOT_PROVIDED] | Expression
    column: str | None
    concrete: bool
    default: Any
    empty_values: Sequence[Any]
    creation_counter: int
    auto_creation_counter: int
    default_validators: list[_ValidatorCallable]
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
        null: _NT = ...,
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
        validators: Iterable[_ValidatorCallable] = (),
        error_messages: _ErrorMessagesMapping | None = None,
        db_comment: str | None = None,
        db_default: type[NOT_PROVIDED] | Expression | _ST = ...,
    ) -> None: ...
    @overload
    @type_check_only
    def __set__(self: Field[Any, Any, Literal[False]], instance: Any, value: _ST | Combinable) -> None: ...
    @overload
    @type_check_only
    def __set__(self: Field[Any, Any, Literal[True]], instance: Any, value: _ST | Combinable | None) -> None: ...
    @overload
    @type_check_only
    def __set__(self, instance: Any, value: _ST | Combinable) -> None: ...
    # class access
    @overload
    @type_check_only
    def __get__(self, instance: None, owner: Any) -> _FieldDescriptor[Self]: ...
    # non-null Model instance access
    @overload
    @type_check_only
    def __get__(self: Field[Any, Any, Literal[False]], instance: Model, owner: Any) -> _GT: ...
    # nullable Model instance access
    @overload
    @type_check_only
    def __get__(self: Field[Any, Any, Literal[True]], instance: Model, owner: Any) -> _GT | None: ...
    # non-Model instances
    @overload
    @type_check_only
    def __get__(self, instance: Any, owner: Any) -> Self: ...
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    def get_col(self, alias: str, output_field: Field | None = None) -> Col: ...
    @cached_property
    def cached_col(self) -> Col: ...
    def select_format(self, compiler: SQLCompiler, sql: str, params: _ParamsT) -> _AsSqlType: ...
    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]: ...
    def clone(self) -> Self: ...
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __deepcopy__(self, memodict: dict[int, Any]) -> Self: ...
    def __copy__(self) -> Self: ...
    def get_pk_value_on_save(self, instance: Model) -> Any: ...
    def to_python(self, value: Any) -> Any: ...
    @cached_property
    def error_messages(self) -> _ErrorMessagesDict: ...
    @cached_property
    def validators(self) -> list[_ValidatorCallable]: ...
    def run_validators(self, value: Any) -> None: ...
    def validate(self, value: Any, model_instance: Model | None) -> None: ...
    def clean(self, value: Any, model_instance: Model | None) -> Any: ...
    def db_type_parameters(self, connection: BaseDatabaseWrapper) -> DictWrapper: ...
    def db_check(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def db_type(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def rel_db_type(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def cast_db_type(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def db_parameters(self, connection: BaseDatabaseWrapper) -> dict[str, str | None]: ...
    def db_type_suffix(self, connection: BaseDatabaseWrapper) -> str | None: ...
    def get_db_converters(self, connection: BaseDatabaseWrapper) -> list[Callable[..., Any]]: ...
    @cached_property
    def unique(self) -> bool: ...
    @property
    def db_tablespace(self) -> str: ...
    @property
    def db_returning(self) -> bool: ...
    descriptor_class: type
    def set_attributes_from_name(self, name: str) -> None: ...
    def contribute_to_class(self, cls: type[Model], name: str, private_only: bool = False) -> None: ...
    def get_filter_kwargs_for_object(self, obj: Model) -> dict[str, Any]: ...
    def get_attname(self) -> str: ...
    def get_attname_column(self) -> tuple[str, str | None]: ...
    def get_internal_type(self) -> str: ...
    def pre_save(self, model_instance: Model, add: bool) -> Any: ...
    def get_prep_value(self, value: Any) -> Any: ...
    def get_db_prep_value(self, value: Any, connection: BaseDatabaseWrapper, prepared: bool = False) -> Any: ...
    def get_db_prep_save(self, value: Any, connection: BaseDatabaseWrapper) -> Any: ...
    def has_default(self) -> bool: ...
    def has_db_default(self) -> bool: ...
    def get_default(self) -> Any: ...
    def get_choices(
        self,
        include_blank: bool = True,
        blank_choice: _ChoicesList = ...,
        limit_choices_to: _LimitChoicesTo | None = None,
        ordering: Sequence[_OrderByFieldName] = (),
    ) -> BlankChoiceIterator | _ChoicesList: ...
    def value_to_string(self, obj: Model) -> str: ...
    @property
    def flatchoices(self) -> list[_Choice]: ...
    def save_form_data(self, instance: Model, data: Any) -> None: ...
    def formfield(
        self,
        form_class: type[forms.Field] | None = None,
        choices_form_class: type[forms.ChoiceField] | None = None,
        **kwargs: Any,
    ) -> forms.Field | None: ...
    def value_from_object(self, obj: Model) -> _GT: ...
    def slice_expression(self, expression: Expression, start: int, length: int | None) -> Func: ...

_ST_Int = TypeVar("_ST_Int", contravariant=True, default=float | int | str)
_GT_Int = TypeVar("_GT_Int", covariant=True, default=int)

class IntegerField(Field[_ST_Int, _GT_Int, _NT]):
    _pyi_lookup_exact_type: str | int
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class PositiveIntegerRelDbTypeMixin:
    def rel_db_type(self, connection: BaseDatabaseWrapper) -> str: ...

class SmallIntegerField(IntegerField[_ST_Int, _GT_Int, _NT]): ...

class BigIntegerField(IntegerField[_ST_Int, _GT_Int, _NT]):
    MAX_BIGINT: ClassVar[int]
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField[_ST_Int, _GT_Int, _NT]):
    integer_field_class: type[IntegerField]
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, SmallIntegerField[_ST_Int, _GT_Int, _NT]):
    integer_field_class: type[SmallIntegerField]
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class PositiveBigIntegerField(PositiveIntegerRelDbTypeMixin, BigIntegerField[_ST_Int, _GT_Int, _NT]):
    integer_field_class: type[BigIntegerField]
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Float = TypeVar("_ST_Float", contravariant=True, default=float | int | str)
_GT_Float = TypeVar("_GT_Float", covariant=True, default=float)

class FloatField(Field[_ST_Float, _GT_Float, _NT]):
    _pyi_lookup_exact_type: float
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Decimal = TypeVar("_ST_Decimal", contravariant=True, default=str | float | decimal.Decimal)
_GT_Decimal = TypeVar("_GT_Decimal", covariant=True, default=decimal.Decimal)

class DecimalField(Field[_ST_Decimal, _GT_Decimal, _NT]):
    _pyi_lookup_exact_type: str | int | decimal.Decimal
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Decimal = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @cached_property
    def context(self) -> decimal.Context: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Char = TypeVar("_ST_Char", contravariant=True, default=str | int)
_GT_Char = TypeVar("_GT_Char", covariant=True, default=str)

class CharField(Field[_ST_Char, _GT_Char, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Char = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        *,
        db_collation: str | None = None,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class CommaSeparatedIntegerField(CharField[_ST_Char, _GT_Char, _NT]): ...

class SlugField(CharField[_ST_Char, _GT_Char, _NT]):
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: _NT = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Char = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        *,
        max_length: int | None = 50,
        db_index: bool = True,
        allow_unicode: bool = False,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Email = TypeVar("_ST_Email", contravariant=True, default=str)

class EmailField(CharField[_ST_Email, _GT_Char, _NT]):
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class URLField(CharField[_ST_Char, _GT_Char, _NT]):
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: _NT = ...,
        db_index: bool = ...,
        rel: ForeignObjectRel | None = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Char = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Text = TypeVar("_ST_Text", contravariant=True, default=str)
_GT_Text = TypeVar("_GT_Text", covariant=True, default=str)

class TextField(Field[_ST_Text, _GT_Text, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Text = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
        *,
        db_collation: str | None = None,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Bool = TypeVar("_ST_Bool", contravariant=True, default=bool)
_GT_Bool = TypeVar("_GT_Bool", covariant=True, default=bool)

class BooleanField(Field[_ST_Bool, _GT_Bool, _NT]):
    _pyi_lookup_exact_type: bool
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_NBool = TypeVar("_ST_NBool", contravariant=True, default=bool | None)
_GT_NBool = TypeVar("_GT_NBool", covariant=True, default=bool | None)

class NullBooleanField(BooleanField[_ST_NBool, _GT_NBool, _NT]):
    _pyi_lookup_exact_type: bool | None  # type: ignore[assignment]

_ST_IP = TypeVar("_ST_IP", contravariant=True, default=str)
_GT_IP = TypeVar("_GT_IP", covariant=True, default=str)

class IPAddressField(Field[_ST_IP, _GT_IP, _NT]): ...

_ST_GenIP = TypeVar("_ST_GenIP", contravariant=True, default=str | int | Callable[..., Any])

class GenericIPAddressField(Field[_ST_GenIP, _GT_IP, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_GenIP = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class DateTimeCheckMixin:
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...

_ST_Date = TypeVar("_ST_Date", contravariant=True, default=str | date)
_GT_Date = TypeVar("_GT_Date", covariant=True, default=date)

class DateField(DateTimeCheckMixin, Field[_ST_Date, _GT_Date, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Date = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def contribute_to_class(self, cls: type[Model], name: str, **kwargs: Any) -> None: ...  # type: ignore[override]
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Time = TypeVar("_ST_Time", contravariant=True, default=str | time | real_datetime)
_GT_Time = TypeVar("_GT_Time", covariant=True, default=time)

class TimeField(DateTimeCheckMixin, Field[_ST_Time, _GT_Time, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_Time = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_DateTime = TypeVar("_ST_DateTime", contravariant=True, default=str | real_datetime | date)
_GT_DateTime = TypeVar("_GT_DateTime", covariant=True, default=real_datetime)

class DateTimeField(DateField[_ST_DateTime, _GT_DateTime, _NT]):
    _pyi_lookup_exact_type: str | real_datetime
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_UUID = TypeVar("_ST_UUID", contravariant=True, default=str | uuid.UUID)
_GT_UUID = TypeVar("_GT_UUID", covariant=True, default=uuid.UUID)

class UUIDField(Field[_ST_UUID, _GT_UUID, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        rel: ForeignObjectRel | None = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST_UUID = ...,
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
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class FilePathField(Field[_ST, _GT, _NT]):
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
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | _ST = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: _ChoicesInput | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

_ST_Binary = TypeVar("_ST_Binary", contravariant=True, default=bytes | bytearray | memoryview)
_GT_Binary = TypeVar("_GT_Binary", covariant=True, default=bytes | memoryview)

class BinaryField(Field[_ST_Binary, _GT_Binary, _NT]):
    def get_placeholder(self, value: Any, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> str: ...

_ST_Duration = TypeVar("_ST_Duration", contravariant=True, default=str | timedelta)
_GT_Duration = TypeVar("_GT_Duration", covariant=True, default=timedelta)

class DurationField(Field[_ST_Duration, _GT_Duration, _NT]):
    @override
    def formfield(self, **kwargs: Any) -> forms.Field | None: ...  # type: ignore[override]

class AutoFieldMixin:
    db_returning: bool
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]: ...
    def validate(self, value: Any, model_instance: Model | None) -> None: ...
    def get_db_prep_value(self, value: Any, connection: BaseDatabaseWrapper, prepared: bool = False) -> Any: ...
    def contribute_to_class(self, cls: type[Model], name: str, **kwargs: Any) -> None: ...
    def formfield(self, **kwargs: Any) -> None: ...

class AutoFieldMeta(type): ...

_ST_Auto = TypeVar("_ST_Auto", contravariant=True, default=int | str)
_GT_Auto = TypeVar("_GT_Auto", covariant=True, default=int)

class AutoField(AutoFieldMixin, IntegerField[_ST_Auto, _GT_Auto, _NT], metaclass=AutoFieldMeta):  # type: ignore[misc]
    _pyi_lookup_exact_type: str | int

class BigAutoField(AutoFieldMixin, BigIntegerField[_ST_Auto, _GT_Auto, _NT]): ...  # type: ignore[misc]
class SmallAutoField(AutoFieldMixin, SmallIntegerField[_ST_Auto, _GT_Auto, _NT]): ...  # type: ignore[misc]

__all__ = [
    "BLANK_CHOICE_DASH",
    "NOT_PROVIDED",
    "AutoField",
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
