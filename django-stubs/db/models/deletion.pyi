from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

from django.db import IntegrityError
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.utils.datastructures import _IndexableCollection

def CASCADE(
    collector: "Collector",
    field: Field[Any, Any],
    sub_objs: QuerySet[Model],
    using: str,
) -> None: ...
def SET_NULL(
    collector: "Collector",
    field: Field[Any, Any],
    sub_objs: QuerySet[Model],
    using: str,
) -> None: ...
def SET_DEFAULT(
    collector: "Collector",
    field: Field[Any, Any],
    sub_objs: QuerySet[Model],
    using: str,
) -> None: ...
def DO_NOTHING(
    collector: "Collector",
    field: Field[Any, Any],
    sub_objs: QuerySet[Model],
    using: str,
) -> None: ...
def PROTECT(
    collector: "Collector",
    field: Field[Any, Any],
    sub_objs: QuerySet[Model],
    using: str,
) -> None: ...
def RESTRICT(
    collector: "Collector",
    field: Field[Any, Any],
    sub_objs: QuerySet[Model],
    using: str,
) -> None: ...
def SET(value: Any) -> Callable[..., Any]: ...
def get_candidate_relations_to_delete(opts: Options) -> Iterable[Field]: ...

class ProtectedError(IntegrityError):
    protected_objects: Set[Model]
    def __init__(self, msg: str, protected_objects: Set[Model]) -> None: ...

class RestrictedError(IntegrityError):
    restricted_objects: Set[Model]
    def __init__(self, msg: str, restricted_objects: Set[Model]) -> None: ...

class Collector:
    using: str
    data: Any
    field_updates: Any
    restricted_objects: Any
    fast_deletes: Any
    dependencies: Any
    def __init__(self, using: str) -> None: ...
    def add(
        self,
        objs: _IndexableCollection[Model],
        source: Optional[Type[Model]] = ...,
        nullable: bool = ...,
        reverse_dependency: bool = ...,
    ) -> List[Model]: ...
    def add_dependency(self, model: Type[Model], dependency: Type[Model], reverse_dependency: bool = ...) -> None: ...
    def add_field_update(self, field: Field, value: Any, objs: _IndexableCollection[Model]) -> None: ...
    def add_restricted_objects(self, field: Field, objs: _IndexableCollection[Model]) -> None: ...
    def clear_restricted_objects_from_set(self, model: Type[Model], objs: Set[Model]) -> None: ...
    def clear_restricted_objects_from_queryset(self, model: Type[Model], qs: QuerySet[Model]) -> None: ...
    def can_fast_delete(self, objs: Union[Model, Iterable[Model]], from_field: Optional[Field] = ...) -> bool: ...
    def get_del_batches(
        self, objs: _IndexableCollection[Model], fields: Iterable[Field]
    ) -> Sequence[Sequence[Model]]: ...
    def collect(
        self,
        objs: _IndexableCollection[Optional[Model]],
        source: Optional[Type[Model]] = ...,
        nullable: bool = ...,
        collect_related: bool = ...,
        source_attr: Optional[str] = ...,
        reverse_dependency: bool = ...,
        keep_parents: bool = ...,
        fail_on_restricted: bool = ...,
    ) -> None: ...
    def related_objects(
        self, related_model: Type[Model], related_fields: Iterable[Field], objs: _IndexableCollection[Model]
    ) -> QuerySet[Model]: ...
    def instances_with_model(self) -> Iterator[Tuple[Type[Model], Model]]: ...
    def sort(self) -> None: ...
    def delete(self) -> Tuple[int, Dict[str, int]]: ...
