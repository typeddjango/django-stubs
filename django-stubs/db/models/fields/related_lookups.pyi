from collections.abc import Iterable, Mapping
from typing import Any

from django.db.models.fields import Field
from django.db.models.lookups import (
    Exact,
    GreaterThan,
    GreaterThanOrEqual,
    In,
    IsNull,
    LessThan,
    LessThanOrEqual,
    Lookup,
)

class MultiColSource:
    alias: str
    field: Field[Any, Any]
    sources: tuple[Field[Any, Any], Field[Any, Any]]
    targets: tuple[Field[Any, Any], Field[Any, Any]]
    contains_aggregate: bool
    output_field: Field[Any, Any]
    def __init__(
        self,
        alias: str,
        targets: tuple[Field[Any, Any], Field[Any, Any]],
        sources: tuple[Field[Any, Any], Field[Any, Any]],
        field: Field[Any, Any],
    ) -> None: ...
    def relabeled_clone(self, relabels: Mapping[str, str]) -> MultiColSource: ...
    def get_lookup(self, lookup: str) -> type[Lookup[Any]] | None: ...

def get_normalized_value(value: Any, lhs: Any) -> tuple[Any, ...]: ...

class RelatedIn(In):
    bilateral_transforms: list[Any]
    lhs: Any
    rhs: Any
    def get_prep_lookup(self) -> Iterable[Any]: ...

class RelatedLookupMixin:
    rhs: Any
    def get_prep_lookup(self) -> Any: ...

class RelatedExact(RelatedLookupMixin, Exact[Any]): ...
class RelatedLessThan(RelatedLookupMixin, LessThan[Any]): ...
class RelatedGreaterThan(RelatedLookupMixin, GreaterThan[Any]): ...
class RelatedGreaterThanOrEqual(RelatedLookupMixin, GreaterThanOrEqual[Any]): ...
class RelatedLessThanOrEqual(RelatedLookupMixin, LessThanOrEqual[Any]): ...
class RelatedIsNull(RelatedLookupMixin, IsNull): ...
