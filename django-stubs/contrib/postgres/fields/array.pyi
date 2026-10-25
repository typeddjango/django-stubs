from collections.abc import Sequence
from typing import Any, ClassVar, Literal, overload

from _typeshed import Unused
from django.contrib.postgres.utils import CheckPostgresInstalledMixin
from django.core.checks import CheckMessage
from django.core.validators import _ValidatorCallable
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field
from django.db.models.expressions import Expression
from django.db.models.fields import NOT_PROVIDED, FieldInitKwargs, _ErrorMessagesDict
from django.db.models.fields.mixins import CheckFieldDefaultMixin
from django.db.models.lookups import Transform
from django.db.models.sql.compiler import _AsSqlType
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeVar, Unpack, override

# The column's set and get types, like every other field. The `__init__` overloads fill them
# from `base_field`'s own type parameters, so the element type never needs spelling out.
_ST_Array = TypeVar("_ST_Array", contravariant=True, default=Sequence[Any])
_GT_Array = TypeVar("_GT_Array", covariant=True, default=list[Any])
# Element set and get types, solved from the `base_field` argument.
_ElemST = TypeVar("_ElemST")
_ElemGT = TypeVar("_ElemGT")

class ArrayField(CheckPostgresInstalledMixin, CheckFieldDefaultMixin, Field[_ST_Array, _GT_Array]):
    empty_strings_allowed: bool
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: Field[Any, Any]
    size: int | None
    default_validators: list[_ValidatorCallable]
    from_db_value: Any
    @overload
    def __init__(
        self: ArrayField[Sequence[_ElemST] | None, list[_ElemGT] | None],
        base_field: Field[_ElemST, _ElemGT],
        size: int | None = None,
        *,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @overload
    def __init__(
        self: ArrayField[Sequence[_ElemST], list[_ElemGT]],
        base_field: Field[_ElemST, _ElemGT],
        size: int | None = None,
        *,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        null: bool = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @override
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    @property
    @override
    def description(self) -> str: ...  # type: ignore[override]
    @override
    def cast_db_type(self, connection: BaseDatabaseWrapper) -> str: ...
    def get_placeholder_sql(self, value: Unused, compiler: Unused, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    @override
    def get_transform(self, name: str) -> type[Transform] | None: ...

__all__ = ["ArrayField"]
