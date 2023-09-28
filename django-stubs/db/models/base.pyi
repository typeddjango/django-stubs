from collections.abc import Collection, Iterable, Sequence
from typing import Any, ClassVar, Final, TypeVar, overload

from django.core.checks.messages import CheckMessage
from django.core.exceptions import MultipleObjectsReturned as BaseMultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import BaseConstraint, Field
from django.db.models.manager import BaseManager, Manager
from django.db.models.options import Options
from typing_extensions import Self

_Self = TypeVar("_Self", bound=Model)

class ModelStateFieldsCacheDescriptor:
    @overload
    def __get__(self, inst: None, owner: object) -> Self: ...
    @overload
    def __get__(self, inst: object, owner: object) -> dict[Any, Any]: ...

class ModelState:
    db: str | None
    adding: bool
    fields_cache: ModelStateFieldsCacheDescriptor

class ModelBase(type):
    @property
    def _default_manager(cls: type[_Self]) -> BaseManager[_Self]: ...  # type: ignore[misc]
    @property
    def _base_manager(cls: type[_Self]) -> BaseManager[_Self]: ...  # type: ignore[misc]

class Model(metaclass=ModelBase):
    # Note: these two metaclass generated attributes don't really exist on the 'Model'
    # class, runtime they are only added on concrete subclasses of 'Model'. The
    # metaclass also sets up correct inheritance from concrete parent models exceptions.
    # Our mypy plugin aligns with this behaviour and will remove the 2 attributes below
    # and re-add them to correct concrete subclasses of 'Model'
    DoesNotExist: Final[type[ObjectDoesNotExist]]
    MultipleObjectsReturned: Final[type[BaseMultipleObjectsReturned]]
    # This 'objects' attribute will be deleted, via the plugin, in favor of managing it
    # to only exist on subclasses it exists on during runtime.
    objects: ClassVar[Manager[Self]]

    class Meta: ...
    _meta: ClassVar[Options[Self]]
    pk: Any
    _state: ModelState
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def add_to_class(cls, name: str, value: Any) -> Any: ...
    @classmethod
    def from_db(cls, db: str | None, field_names: Collection[str], values: Collection[Any]) -> Self: ...
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]: ...
    async def adelete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]: ...
    def full_clean(
        self, exclude: Iterable[str] | None = ..., validate_unique: bool = ..., validate_constraints: bool = ...
    ) -> None: ...
    def clean(self) -> None: ...
    def clean_fields(self, exclude: Collection[str] | None = ...) -> None: ...
    def validate_unique(self, exclude: Collection[str] | None = ...) -> None: ...
    def date_error_message(self, lookup_type: str, field_name: str, unique_for: str) -> ValidationError: ...
    def unique_error_message(self, model_class: type[Self], unique_check: Sequence[str]) -> ValidationError: ...
    def validate_constraints(self, exclude: Collection[str] | None = ...) -> None: ...
    def get_constraints(self) -> list[tuple[type[Model], Sequence[BaseConstraint]]]: ...
    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None: ...
    async def asave(
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
    def refresh_from_db(self, using: str | None = ..., fields: Sequence[str] | None = ...) -> None: ...
    async def arefresh_from_db(self, using: str | None = ..., fields: Sequence[str] | None = ...) -> None: ...
    def serializable_value(self, field_name: str) -> Any: ...
    def prepare_database_save(self, field: Field) -> Any: ...
    def get_deferred_fields(self) -> set[str]: ...
    @classmethod
    def check(cls, **kwargs: Any) -> list[CheckMessage]: ...
    def __getstate__(self) -> dict: ...

def model_unpickle(model_id: tuple[str, str] | type[Model]) -> Model: ...
