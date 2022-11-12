from typing import Any, Iterable, List, Mapping, Tuple, Type

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
    field: Field
    sources: Tuple[Field, Field]
    targets: Tuple[Field, Field]
    contains_aggregate: bool
    output_field: Field
    def __init__(
        self, alias: str, targets: Tuple[Field, Field], sources: Tuple[Field, Field], field: Field
    ) -> None: ...
    def relabeled_clone(self, relabels: Mapping[str, str]) -> MultiColSource: ...
    def get_lookup(self, lookup: str) -> Type[Lookup] | None: ...

def get_normalized_value(value: Any, lhs: Any) -> Tuple[Any, ...]: ...

class RelatedIn(In):
    bilateral_transforms: List[Any]
    lhs: Any
    rhs: Any
    def get_prep_lookup(self) -> Iterable[Any]: ...

class RelatedLookupMixin:
    rhs: Any
    def get_prep_lookup(self) -> Any: ...

class RelatedExact(RelatedLookupMixin, Exact): ...
class RelatedLessThan(RelatedLookupMixin, LessThan): ...
class RelatedGreaterThan(RelatedLookupMixin, GreaterThan): ...
class RelatedGreaterThanOrEqual(RelatedLookupMixin, GreaterThanOrEqual): ...
class RelatedLessThanOrEqual(RelatedLookupMixin, LessThanOrEqual): ...
class RelatedIsNull(RelatedLookupMixin, IsNull): ...
