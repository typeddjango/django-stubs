from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.options import Options
from django.db.models.query import QuerySet
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)


def CASCADE(
    collector: Collector,
    field: ForeignKey,
    sub_objs: QuerySet,
    using: str
) -> None: ...


def SET(value: int) -> Callable: ...


def SET_DEFAULT(
    collector: Collector,
    field: ForeignKey,
    sub_objs: QuerySet,
    using: str
) -> None: ...


def SET_NULL(
    collector: Collector,
    field: ForeignKey,
    sub_objs: QuerySet,
    using: str
) -> None: ...


def get_candidate_relations_to_delete(opts: Options) -> Iterator[Any]: ...


class Collector:
    def __init__(self, using: str) -> None: ...
    def add(
        self,
        objs: Any,
        source: Any = ...,
        nullable: bool = ...,
        reverse_dependency: bool = ...
    ) -> Any: ...
    def add_field_update(
        self,
        field: ForeignKey,
        value: Optional[int],
        objs: QuerySet
    ) -> None: ...
    def can_fast_delete(
        self,
        objs: Any,
        from_field: Optional[ForeignKey] = ...
    ) -> bool: ...
    def collect(
        self,
        objs: Any,
        source: Any = ...,
        nullable: bool = ...,
        collect_related: bool = ...,
        source_attr: Optional[str] = ...,
        reverse_dependency: bool = ...,
        keep_parents: bool = ...
    ) -> None: ...
    def delete(self) -> Union[Tuple[int, Dict[Any, Any]], Tuple[int, Dict[str, int]]]: ...
    def get_del_batches(self, objs: Any, field: ForeignKey) -> Any: ...
    def instances_with_model(self) -> Iterator[Any]: ...
    def related_objects(
        self,
        related: ManyToOneRel,
        objs: Any
    ) -> QuerySet: ...
    def sort(self) -> None: ...


class ProtectedError:
    def __init__(
        self,
        msg: str,
        protected_objects: Union[QuerySet, List[Model]]
    ) -> None: ...