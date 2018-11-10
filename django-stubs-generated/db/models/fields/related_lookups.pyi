from collections import OrderedDict
from typing import Any, List, Optional, Tuple, Type, Union
from uuid import UUID

from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db.models.base import Model
from django.db.models.expressions import Col
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignObject
from django.db.models.lookups import (BuiltinLookup, Exact, GreaterThan,
                                      GreaterThanOrEqual, In, IsNull, LessThan,
                                      LessThanOrEqual)
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query


class MultiColSource:
    alias: str
    field: django.db.models.fields.related.ForeignObject
    sources: Tuple[django.db.models.fields.Field, django.db.models.fields.Field]
    targets: Tuple[django.db.models.fields.Field, django.db.models.fields.Field]
    contains_aggregate: bool = ...
    output_field: django.db.models.fields.related.ForeignObject = ...
    def __init__(
        self,
        alias: str,
        targets: Tuple[Field, Field],
        sources: Tuple[Field, Field],
        field: related.ForeignObject,
    ) -> None: ...
    def relabeled_clone(self, relabels: OrderedDict) -> MultiColSource: ...
    def get_lookup(self, lookup: str) -> Type[BuiltinLookup]: ...

def get_normalized_value(
    value: Any, lhs: Union[Col, MultiColSource]
) -> Tuple[None]: ...

class RelatedIn(In):
    bilateral_transforms: List[Any]
    contains_aggregate: bool
    lhs: Union[
        django.db.models.expressions.Col,
        django.db.models.fields.related_lookups.MultiColSource,
    ]
    rhs: Union[
        List[django.db.models.base.Model],
        List[int],
        List[uuid.UUID],
        Set[django.contrib.contenttypes.models.ContentType],
        Set[int],
        Set[str],
        Set[uuid.UUID],
        django.db.models.sql.query.Query,
    ] = ...
    def get_prep_lookup(
        self
    ) -> Union[List[Model], List[int], List[str], List[UUID], Query]: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Any]]: ...

class RelatedLookupMixin:
    rhs: Any = ...
    def get_prep_lookup(self) -> Any: ...
    def as_sql(
        self, compiler: SQLCompiler, connection: DatabaseWrapper
    ) -> Tuple[str, List[Union[int, str]]]: ...

class RelatedExact(RelatedLookupMixin, Exact): ...
class RelatedLessThan(RelatedLookupMixin, LessThan): ...
class RelatedGreaterThan(RelatedLookupMixin, GreaterThan): ...
class RelatedGreaterThanOrEqual(RelatedLookupMixin, GreaterThanOrEqual): ...
class RelatedLessThanOrEqual(RelatedLookupMixin, LessThanOrEqual): ...
class RelatedIsNull(RelatedLookupMixin, IsNull): ...
