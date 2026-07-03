from collections.abc import Iterable, Sequence
from typing import Any, ClassVar

from _typeshed import Unused
from django.contrib.postgres.utils import CheckPostgresInstalledMixin
from django.core.checks import CheckMessage
from django.core.validators import _ValidatorCallable
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Field
from django.db.models.expressions import Combinable, Expression
from django.db.models.fields import _NT, NOT_PROVIDED, _ErrorMessagesDict, _ErrorMessagesMapping
from django.db.models.fields.mixins import CheckFieldDefaultMixin
from django.db.models.lookups import Transform
from django.utils.choices import _Choices
from django.utils.functional import _StrOrPromise
from typing_extensions import TypeVar, override

_ST_Array = TypeVar("_ST_Array", contravariant=True, default=Any)
_GT_Array = TypeVar("_GT_Array", covariant=True, default=Any)

class ArrayField(
    CheckPostgresInstalledMixin, CheckFieldDefaultMixin, Field[Sequence[_ST_Array] | Combinable, list[_GT_Array], _NT]
):
    empty_strings_allowed: bool
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: Field[_ST_Array, _GT_Array, Any]
    size: int | None
    default_validators: list[_ValidatorCallable]
    from_db_value: Any
    def __init__(
        self,
        base_field: Field[_ST_Array, _GT_Array, Any],
        size: int | None = None,
        *,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: _NT = ...,
        db_index: bool = ...,
        default: Any = ...,
        db_default: type[NOT_PROVIDED] | Expression | list[_ST_Array] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _Choices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_comment: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesMapping | None = ...,
    ) -> None: ...
    @override
    def check(self, **kwargs: Any) -> list[CheckMessage]: ...
    @property
    @override
    def description(self) -> str: ...  # type: ignore[override]
    @override
    def cast_db_type(self, connection: BaseDatabaseWrapper) -> str: ...
    def get_placeholder(self, value: Unused, compiler: Unused, connection: BaseDatabaseWrapper) -> str: ...
    @override
    def get_transform(self, name: str) -> type[Transform] | None: ...
    @override
    def formfield(self, **kwargs: Any) -> Any: ...  # type: ignore[override]

__all__ = ["ArrayField"]
