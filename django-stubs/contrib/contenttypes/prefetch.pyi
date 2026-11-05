from collections.abc import Sequence
from typing import Any, Generic

from django.db.models import Model, Prefetch
from django.db.models.query import QuerySet
from typing_extensions import TypeVar, override

# The type of the lookup passed to Prefetch(...)
# This will be specialized to a `LiteralString` in the plugin for further processing and validation
_LookupT_co = TypeVar("_LookupT_co", bound=str, covariant=True)
# The type of the querysets passed to GenericPrefetch(...)
_PrefetchedQuerySetsT_co = TypeVar(
    "_PrefetchedQuerySetsT_co", bound=Sequence[QuerySet[Model]], covariant=True, default=list[QuerySet[Model]]
)
# The attribute name to store the prefetched list[_PrefetchedQuerySetT]
# This will be specialized to a `LiteralString` in the plugin for further processing and validation
_ToAttrT_co = TypeVar("_ToAttrT_co", bound=str, covariant=True, default=str)

class GenericPrefetch(Prefetch[Any, Any, Any], Generic[_LookupT_co, _PrefetchedQuerySetsT_co, _ToAttrT_co]):
    def __init__(
        self, lookup: _LookupT_co, querysets: _PrefetchedQuerySetsT_co, to_attr: _ToAttrT_co | None = None
    ) -> None: ...
    @override
    def __getstate__(self) -> dict[str, Any]: ...
    @override
    def get_current_querysets(self, level: int) -> _PrefetchedQuerySetsT_co | None: ...
