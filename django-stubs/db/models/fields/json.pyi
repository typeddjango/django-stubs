import json
from collections.abc import Callable, Iterable
from typing import Any, ClassVar

from django.core import validators
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model, lookups
from django.db.models.expressions import Expression
from django.db.models.fields import _GT, _NT, _ST, NOT_PROVIDED, Field, TextField, _ErrorMessagesMapping
from django.db.models.fields.mixins import CheckFieldDefaultMixin
from django.db.models.lookups import FieldGetDbPrepValueMixin, PostgresOperatorLookup, Transform
from django.db.models.sql.compiler import SQLCompiler, _AsSqlType
from django.utils.choices import _ChoicesInput
from django.utils.functional import _StrOrPromise
from typing_extensions import Self, override

class JSONField(CheckFieldDefaultMixin, Field[_ST, _GT, _NT]):
    encoder: type[json.JSONEncoder] | None
    decoder: type[json.JSONDecoder] | None
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        encoder: type[json.JSONEncoder] | None = None,
        decoder: type[json.JSONDecoder] | None = None,
        *,
        primary_key: bool = ...,
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
        validators: Iterable[validators._ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    def from_db_value(self, value: str | None, expression: Expression, connection: BaseDatabaseWrapper) -> Any: ...
    @override
    def get_transform(self, name: str) -> type[Transform] | KeyTransformFactory: ...  # type: ignore[override]
    @override
    def value_to_string(self, obj: Model) -> Any: ...
    @override
    def formfield(self, **kwargs: Any) -> Any: ...  # type: ignore[override]

class DataContains(FieldGetDbPrepValueMixin, PostgresOperatorLookup): ...
class ContainedBy(FieldGetDbPrepValueMixin, PostgresOperatorLookup): ...

class HasKeyLookup(PostgresOperatorLookup):
    logical_operator: str | None
    def compile_json_path_final_key(self, connection: BaseDatabaseWrapper, key_transform: Any) -> str: ...
    @override
    def as_sql(
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper, template: str | None = None
    ) -> _AsSqlType: ...
    def as_mysql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def as_sqlite(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class HasKey(HasKeyLookup):
    postgres_operator: str

class HasKeys(HasKeyLookup):
    postgres_operator: str
    logical_operator: str

class HasAnyKeys(HasKeys):
    postgres_operator: str
    logical_operator: str

class HasKeyOrArrayIndex(HasKey):
    @override
    def compile_json_path_final_key(self, connection: BaseDatabaseWrapper, key_transform: Any) -> str: ...

class JSONExact(lookups.Exact): ...

class CaseInsensitiveMixin:
    def process_rhs(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class JSONIContains(CaseInsensitiveMixin, lookups.IContains): ...

class KeyTransform(Transform):
    key_name: str
    postgres_operator: str
    postgres_nested_operator: str
    def __init__(self, key_name: Any, *args: Any, **kwargs: Any) -> None: ...
    def preprocess_lhs(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> Any: ...
    def as_mysql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def as_oracle(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    def as_postgresql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    @override
    def as_sqlite(  # type: ignore[override]
        self, compiler: SQLCompiler, connection: BaseDatabaseWrapper
    ) -> _AsSqlType: ...

class KeyTextTransform(KeyTransform):
    postgres_operator: str
    postgres_nested_operator: str
    output_field: ClassVar[TextField]
    @override
    def as_mysql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...
    @classmethod
    def from_lookup(cls, lookup: str) -> Self: ...

KT: Callable[[str], KeyTextTransform]

class KeyTransformTextLookupMixin:
    def __init__(self, key_transform: Any, *args: Any, **kwargs: Any) -> None: ...

class KeyTransformIsNull(lookups.IsNull):
    def as_sqlite(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class KeyTransformIn(lookups.In): ...
class KeyTransformExact(JSONExact): ...
class KeyTransformIExact(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IExact): ...
class KeyTransformIContains(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IContains): ...
class KeyTransformStartsWith(KeyTransformTextLookupMixin, lookups.StartsWith): ...
class KeyTransformIStartsWith(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IStartsWith): ...
class KeyTransformEndsWith(KeyTransformTextLookupMixin, lookups.EndsWith): ...
class KeyTransformIEndsWith(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IEndsWith): ...
class KeyTransformRegex(KeyTransformTextLookupMixin, lookups.Regex): ...
class KeyTransformIRegex(CaseInsensitiveMixin, KeyTransformTextLookupMixin, lookups.IRegex): ...

class KeyTransformNumericLookupMixin:
    def process_rhs(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> _AsSqlType: ...

class KeyTransformLt(KeyTransformNumericLookupMixin, lookups.LessThan): ...
class KeyTransformLte(KeyTransformNumericLookupMixin, lookups.LessThanOrEqual): ...
class KeyTransformGt(KeyTransformNumericLookupMixin, lookups.GreaterThan): ...
class KeyTransformGte(KeyTransformNumericLookupMixin, lookups.GreaterThanOrEqual): ...

class KeyTransformFactory:
    key_name: Any
    def __init__(self, key_name: Any) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> KeyTransform: ...

__all__ = ["JSONField"]
