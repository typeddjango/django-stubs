from typing import Any, Dict, TypeVar

from django.db.models import Expression, Field
from django.db.models.expressions import Combinable, CombinedExpression, Func, Value
from django.db.models.lookups import Lookup

_Expression = str | Combinable | "SearchQueryCombinable"

class SearchVectorExact(Lookup): ...
class SearchVectorField(Field): ...
class SearchQueryField(Field): ...

class SearchConfig(Expression):
    config: _Expression | None
    def __init__(self, config: _Expression) -> None: ...
    @classmethod
    def from_parameter(cls, config: _Expression | None) -> SearchConfig: ...

class SearchVectorCombinable:
    ADD: str

class SearchVector(SearchVectorCombinable, Func):
    config: _Expression | None
    function: str
    arg_joiner: str
    output_field: Field
    def __init__(
        self, *expressions: _Expression, config: _Expression | None = ..., weight: Any | None = ...
    ) -> None: ...

class CombinedSearchVector(SearchVectorCombinable, CombinedExpression):
    def __init__(
        self,
        lhs: Combinable,
        connector: str,
        rhs: Combinable,
        config: _Expression | None,
        output_field: Field | None = None,
    ) -> None: ...

_T = TypeVar("_T", bound="SearchQueryCombinable")

class SearchQueryCombinable:
    BITAND: str
    BITOR: str
    def __or__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __ror__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __and__(self: _T, other: SearchQueryCombinable) -> _T: ...
    def __rand__(self: _T, other: SearchQueryCombinable) -> _T: ...

class SearchQuery(SearchQueryCombinable, Func):  # type: ignore
    SEARCH_TYPES: Dict[str, str]
    def __init__(
        self,
        value: _Expression,
        output_field: Field | None = ...,
        *,
        config: _Expression | None = ...,
        invert: bool = ...,
        search_type: str = ...,
    ) -> None: ...
    def __invert__(self: _T) -> _T: ...

class CombinedSearchQuery(SearchQueryCombinable, CombinedExpression):  # type: ignore
    def __init__(
        self,
        lhs: Combinable,
        connector: str,
        rhs: Combinable,
        config: _Expression | None,
        output_field: Field | None = None,
    ) -> None: ...

class SearchRank(Func):
    def __init__(
        self,
        vector: SearchVector | _Expression,
        query: SearchQuery | _Expression,
        weights: Any | None = ...,
        normalization: Any | None = ...,
        cover_density: bool = ...,
    ) -> None: ...

class SearchHeadline(Func):
    function: str
    template: str
    output_field: Field
    def __init__(
        self,
        expression: _Expression,
        query: _Expression,
        *,
        config: _Expression | None = ...,
        start_sel: Any | None = ...,
        stop_sel: Any | None = ...,
        max_words: int | None = ...,
        min_words: int | None = ...,
        short_word: str | None = ...,
        highlight_all: bool | None = ...,
        max_fragments: int | None = ...,
        fragment_delimiter: str | None = ...,
    ) -> None: ...

class TrigramBase(Func):
    def __init__(self, expression: _Expression, string: str, **extra: Any) -> None: ...

class TrigramSimilarity(TrigramBase):
    function: str

class TrigramDistance(TrigramBase):
    function: str
    arg_joiner: str
