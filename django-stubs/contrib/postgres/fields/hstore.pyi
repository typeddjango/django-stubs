from collections.abc import Mapping
from typing import Any, ClassVar, Literal, overload

from django.contrib.postgres.fields.array import ArrayField
from django.contrib.postgres.utils import CheckPostgresInstalledMixin
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field, TextField, Transform
from django.db.models.expressions import Expression
from django.db.models.fields import NOT_PROVIDED, FieldInitKwargs
from django.db.models.fields.mixins import CheckFieldDefaultMixin
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeVar, Unpack, deprecated, override

# `Mapping` so a `dict[str, str]` is accepted, `dict` is invariant in its values.
_ST_HStore_contra = TypeVar("_ST_HStore_contra", contravariant=True, default=Mapping[str, str | None])
_GT_HStore_co = TypeVar("_GT_HStore_co", covariant=True, default=dict[str, str | None])

class HStoreField(CheckPostgresInstalledMixin, CheckFieldDefaultMixin, Field[_ST_HStore_contra, _GT_HStore_co]):
    # `HStoreField()` or `HStoreField(null=False)`: keeps the type var defaults.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[False] = False,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    # `HStoreField(null=True)`: the `self` annotation gives the nullable type.
    @overload
    def __init__(
        self: HStoreField[Mapping[str, str | None] | None, dict[str, str | None] | None],
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    # `Sub(null=True)` for `class Sub(HStoreField): ...`: its bound types can't match the overload above.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    # `HStoreField(null=flag)` with `flag: bool`. Stays last, as `bool` also matches `True`.
    @overload
    @deprecated("`null` must be a literal `True` or `False` for the field type to be inferred")
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: bool,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs],
    ) -> None: ...
    @override
    def get_transform(self, name: str) -> Any: ...

class KeyTransform(Transform):
    output_field: ClassVar[TextField]

    def __init__(self, key_name: str, *args: Any, **kwargs: Any) -> None: ...
    @override
    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...  # type: ignore[override]

class KeyTransformFactory:
    def __init__(self, key_name: str) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> KeyTransform: ...

class KeysTransform(Transform):
    output_field: ClassVar[ArrayField]

class ValuesTransform(Transform):
    output_field: ClassVar[ArrayField]

__all__ = ["HStoreField"]
