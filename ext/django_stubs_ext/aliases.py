import typing

if typing.TYPE_CHECKING:
    from django.db.models.query import _QuerySet
    from django.utils.functional import _StrOrPromise as StrOrPromise
    from django.utils.functional import _StrPromise as StrPromise

    # Deprecated type aliases. Use the QuerySet class directly instead.
    QuerySetAny = _QuerySet
    ValuesQuerySet = _QuerySet
else:
    from django.db.models.query import QuerySet
    from django.utils.functional import Promise as StrPromise

    StrOrPromise = typing.Union[str, StrPromise]
    # Deprecated type aliases. Use the QuerySet class directly instead.
    QuerySetAny = QuerySet
    ValuesQuerySet = QuerySet

__all__ = ["StrOrPromise", "StrPromise", "QuerySetAny", "ValuesQuerySet"]
