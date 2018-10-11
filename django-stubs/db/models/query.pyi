import decimal
import operator
from collections import OrderedDict
from datetime import date, datetime
from decimal import Decimal
from itertools import chain
from typing import (Any, Callable, Dict, Iterator, List, Optional, Set, Tuple,
                    Type, Union, Generic, TypeVar, overload)
from unittest.mock import MagicMock
from uuid import UUID

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.base import Model, ModelState
from django.db.models.expressions import Expression
from django.db.models.fields import Field
from django.db.models.fields.related_descriptors import (ForwardManyToOneDescriptor,
                                                         ReverseOneToOneDescriptor)
from django.db.models.query_utils import Q
from django.db.models.sql.query import Query, RawQuery

REPR_OUTPUT_SIZE: int
EmptyResultSet: Any


class BaseIterable:
    queryset: Any = ...
    chunked_fetch: Any = ...
    chunk_size: Any = ...

    def __init__(
            self,
            queryset: QuerySet,
            chunked_fetch: bool = ...,
            chunk_size: int = ...,
    ) -> None: ...


class ModelIterable(BaseIterable):
    chunk_size: int
    chunked_fetch: bool
    queryset: QuerySet

    def __iter__(self) -> Iterator[Model]: ...


class ValuesIterable(BaseIterable):
    chunk_size: int
    chunked_fetch: bool
    queryset: QuerySet

    def __iter__(self) -> Iterator[Dict[str, Optional[Union[int, str]]]]: ...


class ValuesListIterable(BaseIterable):
    chunk_size: int
    chunked_fetch: bool
    queryset: QuerySet

    def __iter__(self) -> Union[chain, map]: ...


class NamedValuesListIterable(ValuesListIterable):
    chunk_size: int
    chunked_fetch: bool
    queryset: QuerySet

    @staticmethod
    def create_namedtuple_class(*names: Any) -> Any: ...

    def __iter__(self) -> Any: ...


class FlatValuesListIterable(BaseIterable):
    chunk_size: int
    chunked_fetch: bool
    queryset: QuerySet

    def __iter__(self) -> Iterator[Any]: ...


_T = TypeVar('_T', bound=models.Model)


class QuerySet(Generic[_T]):
    model: Optional[Type[models.Model]] = ...
    query: models.sql.Query = ...

    def __init__(
            self,
            model: Optional[Type[Model]] = ...,
            query: Optional[Query] = ...,
            using: Optional[str] = ...,
            hints: Optional[Dict[str, Model]] = ...,
    ) -> None: ...

    def as_manager(cls): ...

    def __deepcopy__(
            self,
            memo: Dict[
                int,
                Union[
                    Dict[str, Union[ModelState, int, str]],
                    List[Union[Dict[str, Union[bool, str]], ModelState]],
                    Model,
                    ModelState,
                ],
            ],
    ) -> QuerySet[_T]: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[_T]: ...

    def __bool__(self) -> bool: ...

    @overload
    def __getitem__(self, k: slice) -> QuerySet[_T]: ...

    @overload
    def __getitem__(self, k: int) -> _T: ...

    @overload
    def __getitem__(self, k: str) -> Any: ...

    def __and__(self, other: QuerySet) -> QuerySet: ...

    def __or__(self, other: QuerySet) -> QuerySet: ...

    def iterator(self, chunk_size: int = ...) -> Iterator[_T]: ...

    def aggregate(
            self, *args: Any, **kwargs: Any
    ) -> Dict[str, Optional[Union[datetime, float]]]: ...

    def count(self) -> int: ...

    def get(
            self, *args: Any, **kwargs: Any
    ) -> _T: ...

    def create(self, **kwargs: Any) -> _T: ...

    def bulk_create(
            self,
            objs: Union[Iterator[Any], List[Model]],
            batch_size: Optional[int] = ...,
    ) -> List[_T]: ...

    def get_or_create(
            self,
            defaults: Optional[Union[Dict[str, date], Dict[str, Model]]] = ...,
            **kwargs: Any
    ) -> Tuple[_T, bool]: ...

    def update_or_create(
            self,
            defaults: Optional[
                Union[
                    Dict[str, Callable],
                    Dict[str, date],
                    Dict[str, Model],
                    Dict[str, str],
                ]
            ] = ...,
            **kwargs: Any
    ) -> Tuple[_T, bool]: ...

    def earliest(
            self, *fields: Any, field_name: Optional[Any] = ...
    ) -> _T: ...

    def latest(
            self, *fields: Any, field_name: Optional[Any] = ...
    ) -> _T: ...

    def first(self) -> Optional[Union[Dict[str, int], _T]]: ...

    def last(self) -> Optional[_T]: ...

    def in_bulk(
            self, id_list: Any = ..., *, field_name: str = ...
    ) -> Union[Dict[int, Model], Dict[str, Model]]: ...

    def delete(self) -> Tuple[int, Dict[str, int]]: ...

    def update(self, **kwargs: Any) -> int: ...

    def exists(self) -> bool: ...

    def explain(
            self, *, format: Optional[Any] = ..., **options: Any
    ) -> str: ...

    def raw(
            self,
            raw_query: str,
            params: Optional[
                Union[
                    Dict[str, str],
                    List[datetime],
                    List[Decimal],
                    List[str],
                    Set[str],
                    Tuple[int],
                ]
            ] = ...,
            translations: Optional[Dict[str, str]] = ...,
            using: None = ...,
    ) -> RawQuerySet: ...

    def values(self, *fields: Any, **expressions: Any) -> QuerySet: ...

    def values_list(
            self, *fields: Any, flat: bool = ..., named: bool = ...
    ) -> QuerySet: ...

    def dates(
            self, field_name: str, kind: str, order: str = ...
    ) -> QuerySet: ...

    def datetimes(
            self, field_name: str, kind: str, order: str = ..., tzinfo: None = ...
    ) -> QuerySet: ...

    def none(self) -> QuerySet[_T]: ...

    def all(self) -> QuerySet[_T]: ...

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet[_T]: ...

    def exclude(self, *args: Any, **kwargs: Any) -> QuerySet[_T]: ...

    def complex_filter(
            self,
            filter_obj: Union[
                Dict[str, datetime], Dict[str, QuerySet], Q, MagicMock
            ],
    ) -> QuerySet[_T]: ...

    def union(self, *other_qs: Any, all: bool = ...) -> QuerySet[_T]: ...

    def intersection(self, *other_qs: Any) -> QuerySet[_T]: ...

    def difference(self, *other_qs: Any) -> QuerySet[_T]: ...

    def select_for_update(
            self, nowait: bool = ..., skip_locked: bool = ..., of: Tuple = ...
    ) -> QuerySet: ...

    def select_related(self, *fields: Any) -> QuerySet[_T]: ...

    def prefetch_related(self, *lookups: Any) -> QuerySet[_T]: ...

    def annotate(self, *args: Any, **kwargs: Any) -> QuerySet[_T]: ...

    def order_by(self, *field_names: Any) -> QuerySet[_T]: ...

    def distinct(self, *field_names: Any) -> QuerySet[_T]: ...

    def extra(
            self,
            select: Optional[
                Union[Dict[str, int], Dict[str, str], OrderedDict]
            ] = ...,
            where: Optional[List[str]] = ...,
            params: Optional[Union[List[int], List[str]]] = ...,
            tables: Optional[List[str]] = ...,
            order_by: Optional[Union[List[str], Tuple[str]]] = ...,
            select_params: Optional[Union[List[int], List[str], Tuple[int]]] = ...,
    ) -> QuerySet[_T]: ...

    def reverse(self) -> QuerySet[_T]: ...

    def defer(self, *fields: Any) -> QuerySet[_T]: ...

    def only(self, *fields: Any) -> QuerySet[_T]: ...

    def using(self, alias: Optional[str]) -> QuerySet[_T]: ...

    @property
    def ordered(self) -> bool: ...

    @property
    def db(self) -> str: ...

    def resolve_expression(self, *args: Any, **kwargs: Any) -> Query: ...


class InstanceCheckMeta(type):
    def __instancecheck__(self, instance: Union[QuerySet, str]) -> bool: ...


class EmptyQuerySet:
    def __init__(self, *args: Any, **kwargs: Any) -> Any: ...


class RawQuerySet:
    columns: List[str]
    model_fields: Dict[str, models.Field]
    raw_query: str = ...
    model: Optional[Type[models.Model]] = ...
    query: models.sql.RawQuery = ...
    params: Union[
        Dict[str, str],
        List[datetime],
        List[decimal.Decimal],
        List[str],
        Set[str],
        Tuple,
    ] = ...
    translations: Dict[str, str] = ...

    def __init__(
            self,
            raw_query: str,
            model: Optional[Type[Model]] = ...,
            query: Optional[RawQuery] = ...,
            params: Optional[
                Union[
                    Dict[str, str],
                    List[datetime],
                    List[Decimal],
                    List[str],
                    Set[str],
                    Tuple,
                ]
            ] = ...,
            translations: Optional[Dict[str, str]] = ...,
            using: Optional[str] = ...,
            hints: Optional[Dict[Any, Any]] = ...,
    ) -> None: ...

    def resolve_model_init_order(
            self
    ) -> Tuple[List[str], List[int], List[Tuple[str, int]]]: ...

    def prefetch_related(self, *lookups: Any) -> RawQuerySet: ...

    def __len__(self) -> int: ...

    def __bool__(self) -> bool: ...

    def __iter__(self) -> Any: ...

    def iterator(self) -> Iterator[Model]: ...

    def __getitem__(
            self, k: Union[int, slice, str]
    ) -> Union[List[Model], Model]: ...

    @property
    def db(self) -> str: ...

    def using(self, alias: Any): ...

    def columns(self) -> List[str]: ...

    def model_fields(self) -> Dict[str, Field]: ...


class Prefetch:
    prefetch_through: str = ...
    prefetch_to: str = ...
    queryset: Optional[QuerySet] = ...
    to_attr: Optional[str] = ...

    def __init__(
            self,
            lookup: str,
            queryset: Optional[QuerySet] = ...,
            to_attr: Optional[str] = ...,
    ) -> None: ...

    def add_prefix(self, prefix: str) -> None: ...

    def get_current_prefetch_to(self, level: int) -> str: ...

    def get_current_to_attr(self, level: int) -> Tuple[str, Optional[bool]]: ...

    def get_current_queryset(self, level: int) -> Optional[QuerySet]: ...

    def __eq__(self, other: None) -> bool: ...

    def __hash__(self) -> int: ...


def normalize_prefetch_lookups(
        lookups: reversed, prefix: None = ...
) -> List[Prefetch]: ...


def prefetch_related_objects(
        model_instances: Union[List[Model], List[UUID]], *related_lookups: Any
) -> None: ...


def get_prefetcher(
        instance: Model, through_attr: str, to_attr: str
) -> Tuple[
    GenericForeignKey, Union[GenericForeignKey, property], bool, bool
]: ...


def prefetch_one_level(
        instances: List[Model],
        prefetcher: Union[
            GenericForeignKey, ForwardManyToOneDescriptor, ReverseOneToOneDescriptor
        ],
        lookup: Prefetch,
        level: int,
) -> Tuple[List[Model], List[Prefetch]]: ...


class RelatedPopulator:
    db: str = ...
    cols_start: int = ...
    cols_end: int = ...
    init_list: List[str] = ...
    reorder_for_init: Optional[operator.itemgetter] = ...
    model_cls: Type[models.Model] = ...
    pk_idx: int = ...
    related_populators: List[models.query.RelatedPopulator] = ...
    local_setter: Callable = ...
    remote_setter: Callable = ...

    def __init__(
            self,
            klass_info: Dict[str, Any],
            select: List[Tuple[Expression, Tuple[str, List[int]], Optional[str]]],
            db: str,
    ) -> None: ...

    def populate(
            self,
            row: Union[
                List[Optional[Union[date, int, str]]],
                List[Union[date, Decimal, float, str]],
                Tuple[Union[int, str], str, int],
            ],
            from_obj: Model,
    ) -> None: ...


def get_related_populators(
        klass_info: Dict[str, Any],
        select: List[Tuple[Expression, Tuple[str, List[bool]], Optional[str]]],
        db: str,
) -> List[RelatedPopulator]: ...
