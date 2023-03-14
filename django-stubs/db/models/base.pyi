from collections.abc import Collection, Iterable, Sequence
from typing import Any, TypeVar

from _typeshed import Self
from django.core.checks.messages import CheckMessage
from django.core.exceptions import MultipleObjectsReturned as BaseMultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.manager import BaseManager
from django.db.models.options import Options
from typing_extensions import Final

_Self = TypeVar("_Self", bound=Model)

class ModelStateFieldsCacheDescriptor: ...

class ModelState:
    db: str | None
    adding: bool
    fields_cache: ModelStateFieldsCacheDescriptor

class ModelBase(type):
    @property
    def objects(cls: type[_Self]) -> BaseManager[_Self]: ...  # type: ignore[misc]
    @property
    def _default_manager(cls: type[_Self]) -> BaseManager[_Self]: ...  # type: ignore[misc]
    @property
    def _base_manager(cls: type[_Self]) -> BaseManager[_Self]: ...  # type: ignore[misc]

class Model(metaclass=ModelBase):
    DoesNotExist: Final[type[ObjectDoesNotExist]]
    MultipleObjectsReturned: Final[type[BaseMultipleObjectsReturned]]

    class Meta: ...
    _meta: Options[Any]
    pk: Any
    _state: ModelState
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def add_to_class(cls, name: str, value: Any) -> Any: ...
    @classmethod
    def from_db(cls: type[Self], db: str | None, field_names: Collection[str], values: Collection[Any]) -> Self: ...
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]: ...
    def full_clean(
        self, exclude: Iterable[str] | None = ..., validate_unique: bool = ..., validate_constraints: bool = ...
    ) -> None: ...
    def clean(self) -> None: ...
    def clean_fields(self, exclude: Collection[str] | None = ...) -> None: ...
    def validate_unique(self, exclude: Collection[str] | None = ...) -> None: ...
    def unique_error_message(self, model_class: type[Self], unique_check: Sequence[str]) -> ValidationError: ...
    def validate_constraints(self, exclude: Collection[str] | None = ...) -> None: ...
    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None: ...
    def save_base(
        self,
        raw: bool = ...,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None: ...
    def refresh_from_db(self: Self, using: str | None = ..., fields: Sequence[str] | None = ...) -> None: ...
    def get_deferred_fields(self) -> set[str]: ...
    @classmethod
    def check(cls, **kwargs: Any) -> list[CheckMessage]: ...
    def __getstate__(self) -> dict: ...

def model_unpickle(model_id: tuple[str, str] | type[Model]) -> Model: ...
