from typing import Any, Dict, Optional, TypeVar, Union

from django.db.models import Expression, Field
from django.db.models.expressions import Combinable, CombinedExpression, Func, Value
from django.db.models.lookups import Lookup

_Expression = Union[str, Combinable, "SearchQueryCombinable"]

class SearchVectorExact(Lookup): ...
class SearchVectorField(Field): ...
class SearchQueryField(Field): ...

class SearchConfig(Expression):
    config: Optional[_Expression] = ...
    def __init__(self, config: _Expression) -> None: ...
    @classmethod
    def from_parameter(cls, config: Optional[_Expression]) -> SearchConfig: ...

class SearchVectorCombinable:
    ADD: str = ...

class SearchVector(SearchVectorCombinable, Func):
    config: Optional[_Expression] = ...
    function: str = ...
    arg_joiner: str = ...
    output_field: Field
    def __init__(
        self, *expressions: _Expression, config: Optional[_Expression] = ..., weight: Optional[Any] = ...
    ) -> None: ...

class CombinedSearchVector(SearchVectorCombinable, CombinedExpression):
    def __init__(
        self,
        lhs: Combinable,
        connector: str,
        rhs: Combinable,
        config: Optional[_Expression],
        output_field: Optional[Field] = None,
    ) -> None: ...

_T = TypeVar("_T", bound="SearchQueryCombinable")

class SearchQueryCombinable:
    BITAND: str = ...
    BITOR: str = ...
    def __or__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __ror__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __and__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __rand__(self: _T, other: SearchQueryCombinable) -> _T: ...

class SearchQuery(SearchQueryCombinable, Func):  # type: ignore
    SEARCH_TYPES: Dict[str, str] = ...
    def __init__(
        self,
        value: _Expression,
        output_field: Optional[Field] = ...,
        *,
        config: Optional[_Expression] = ...,
        invert: bool = ...,
        search_type: str = ...,
    ): ...
    def __invert__(self: _T) -> _T: ...

class CombinedSearchQuery(SearchQueryCombinable, CombinedExpression):  # type: ignore
    def __init__(
        self,
        lhs: Combinable,
        connector: str,
        rhs: Combinable,
        config: Optional[_Expression],
        output_field: Optional[Field] = None,
    ) -> None: ...

class SearchRank(Func):
    def __init__(
        self,
        vector: Union[SearchVector, _Expression],
        query: Union[SearchQuery, _Expression],
        weights: Optional[Any] = ...,
        normalization: Optional[Any] = ...,
        cover_density: bool = ...,
    ) -> None: ...

class SearchHeadline(Func):
    function: str = ...
    template: str = ...
    output_field: Field = ...
    def __init__(
        self,
        expression: _Expression,
        query: _Expression,
        *,
        config: Optional[_Expression] = ...,
        start_sel: Optional[Any] = ...,
        stop_sel: Optional[Any] = ...,
        max_words: Optional[int] = ...,
        min_words: Optional[int] = ...,
        short_word: Optional[str] = ...,
        highlight_all: Optional[bool] = ...,
        max_fragments: Optional[int] = ...,
        fragment_delimiter: Optional[str] = ...,
    ) -> None: ...

class TrigramBase(Func):
    def __init__(self, expression: _Expression, string: str, **extra: Any) -> None: ...

class TrigramSimilarity(TrigramBase):
    function: str

class TrigramDistance(TrigramBase):
    function: str
    arg_joiner: str
