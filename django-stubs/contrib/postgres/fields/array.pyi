from collections.abc import Sequence
from typing import Any, ClassVar

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

# __set__ value type
_ST = TypeVar("_ST", contravariant=True, default=Any)
# __get__ return type
_GT = TypeVar("_GT", covariant=True, default=Any)

class ArrayField(CheckPostgresInstalledMixin, CheckFieldDefaultMixin, Field[_ST, _GT]):
    _pyi_private_set_type: Sequence[Any]
    _pyi_private_get_type: list[Any]

    empty_strings_allowed: bool
    default_error_messages: ClassVar[_ErrorMessagesDict]
    base_field: Field
    size: int | None
    default_validators: list[_ValidatorCallable]
    from_db_value: Any
    def __init__(
        self,
        base_field: Field,
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
