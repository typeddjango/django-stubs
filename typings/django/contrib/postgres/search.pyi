from typing import Any, Dict, Optional, TypeVar, Union

from django.db.models import Field
from django.db.models.expressions import (
    Combinable,
    CombinedExpression,
    Func,
    Value,
    _OutputField,
)
from django.db.models.lookups import Lookup

_Expression = Union[str, Combinable, "SearchQueryCombinable"]

class SearchVectorExact(Lookup[Any]): ...
class SearchVectorField(Field[Any, Any]): ...
class SearchQueryField(Field[Any, Any]): ...

class SearchVectorCombinable:
    ADD: str = ...

class SearchVector(SearchVectorCombinable, Func):
    config: Optional[Any] = ...
    def __init__(self, *expressions: _Expression, **extra: Any) -> None: ...

class CombinedSearchVector(SearchVectorCombinable, CombinedExpression):
    def __init__(
        self,
        lhs: Any,
        connector: Any,
        rhs: Any,
        config: Optional[_Expression] = ...,
        output_field: Optional[_OutputField] = ...,
    ) -> None: ...

_T = TypeVar("_T", bound="SearchQueryCombinable")

class SearchQueryCombinable:
    BITAND: str = ...
    BITOR: str = ...
    def __or__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __ror__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __and__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __rand__(self: _T, other: SearchQueryCombinable) -> _T: ...

class SearchQuery(SearchQueryCombinable, Value):  # type: ignore
    SEARCH_TYPES: Dict[str, str] = ...
    def __init__(
        self,
        value: str,
        output_field: Optional[_OutputField] = ...,
        *,
        config: Optional[_Expression] = ...,
        invert: bool = ...,
        search_type: str = ...
    ) -> None: ...
    def __invert__(self: _T) -> _T: ...

class CombinedSearchQuery(SearchQueryCombinable, CombinedExpression):  # type: ignore
    def __init__(
        self,
        lhs: Any,
        connector: Any,
        rhs: Any,
        config: Optional[_Expression] = ...,
        output_field: Optional[_OutputField] = ...,
    ) -> None: ...

class SearchRank(Func):
    def __init__(
        self,
        vector: Union[SearchVector, _Expression],
        query: Union[SearchQuery, _Expression],
        **extra: Any
    ) -> None: ...

class TrigramBase(Func):
    def __init__(self, expression: _Expression, string: str, **extra: Any) -> None: ...

class TrigramSimilarity(TrigramBase): ...
class TrigramDistance(TrigramBase): ...
