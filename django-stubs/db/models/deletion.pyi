from django.contrib.auth.models import (
    Permission,
    User,
)
from django.contrib.contenttypes.models import ContentType
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
    Type,
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
        source: Optional[Union[Type[Model], Type[ContentType]]] = ...,
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
        source: Optional[Union[Type[Model], Type[ContentType]]] = ...,
        nullable: bool = ...,
        collect_related: bool = ...,
        source_attr: Optional[str] = ...,
        reverse_dependency: bool = ...,
        keep_parents: bool = ...
    ) -> None: ...
    def delete(self) -> Union[Tuple[int, Dict[str, int]], Tuple[int, Dict[Any, Any]]]: ...
    def get_del_batches(
        self,
        objs: Union[List[User], List[Model], List[ContentType], List[Permission]],
        field: ForeignKey
    ) -> Union[List[List[Model]], List[List[ContentType]], List[List[User]], List[List[Permission]]]: ...
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
        protected_objects: Union[List[Model], QuerySet]
    ) -> None: ...