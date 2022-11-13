from collections.abc import Iterable, Sequence
from typing import Any, TypeVar

from django.core.validators import _ValidatorCallable
from django.db.models import Field, Transform
from django.db.models.expressions import Combinable
from django.db.models.fields import _ErrorMessagesT, _FieldChoices
from django.db.models.fields.mixins import CheckFieldDefaultMixin
from django.utils.functional import _StrOrPromise

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class ArrayField(CheckFieldDefaultMixin, Field[_ST, _GT]):
    _pyi_private_set_type: Sequence[Any] | Combinable
    _pyi_private_get_type: list[Any]

    empty_strings_allowed: bool
    default_error_messages: _ErrorMessagesT
    base_field: Field
    size: int | None
    default_validators: Sequence[_ValidatorCallable]
    from_db_value: Any
    def __init__(
        self,
        base_field: Field,
        size: int | None = ...,
        *,
        verbose_name: _StrOrPromise | None = ...,
        name: str | None = ...,
        primary_key: bool = ...,
        max_length: int | None = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: str | None = ...,
        unique_for_month: str | None = ...,
        unique_for_year: str | None = ...,
        choices: _FieldChoices | None = ...,
        help_text: _StrOrPromise = ...,
        db_column: str | None = ...,
        db_tablespace: str | None = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: _ErrorMessagesT | None = ...,
    ) -> None: ...
    @property
    def description(self) -> str: ...  # type: ignore
    def get_transform(self, name: Any) -> type[Transform] | None: ...
