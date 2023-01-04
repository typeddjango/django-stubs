from typing import Any

from _typeshed import Self
from django.db.models import Expression, Field
from django.db.models.expressions import Combinable, CombinedExpression, Func
from django.db.models.lookups import Lookup
from typing_extensions import TypeAlias

_Expression: TypeAlias = str | Combinable | SearchQueryCombinable

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
        output_field: Field | None = ...,
    ) -> None: ...

class SearchQueryCombinable:
    BITAND: str
    BITOR: str
    def __or__(self: Self, other: SearchQueryCombinable) -> Self: ...
    def __ror__(self: Self, other: SearchQueryCombinable) -> Self: ...
    def __and__(self: Self, other: SearchQueryCombinable) -> Self: ...
    def __rand__(self: Self, other: SearchQueryCombinable) -> Self: ...

class SearchQuery(SearchQueryCombinable, Func):  # type: ignore
    SEARCH_TYPES: dict[str, str]
    def __init__(
        self,
        value: _Expression,
        output_field: Field | None = ...,
        *,
        config: _Expression | None = ...,
        invert: bool = ...,
        search_type: str = ...,
    ) -> None: ...
    def __invert__(self: Self) -> Self: ...

class CombinedSearchQuery(SearchQueryCombinable, CombinedExpression):  # type: ignore
    def __init__(
        self,
        lhs: Combinable,
        connector: str,
        rhs: Combinable,
        config: _Expression | None,
        output_field: Field | None = ...,
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

class TrigramWordBase(Func):
    def __init__(self, string: str, expression: _Expression, **extra: Any) -> None: ...

class TrigramSimilarity(TrigramBase): ...
class TrigramDistance(TrigramBase): ...
class TrigramWordDistance(TrigramWordBase): ...
class TrigramStrictWordDistance(TrigramWordBase): ...
class TrigramWordSimilarity(TrigramWordBase): ...
class TrigramStrictWordSimilarity(TrigramWordBase): ...
