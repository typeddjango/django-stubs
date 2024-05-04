import typing

if typing.TYPE_CHECKING:
    from django.db.models.query import _QuerySet
    from django.utils.functional import _StrOrPromise as StrOrPromise
    from django.utils.functional import _StrPromise as StrPromise

    QuerySetAny = _QuerySet
    ValuesQuerySet = _QuerySet
else:
    from django.db.models.query import QuerySet
    from django.utils.functional import Promise as StrPromise

    QuerySetAny = QuerySet
    ValuesQuerySet = QuerySet
    StrOrPromise = typing.Union[str, StrPromise]

__all__ = ["StrOrPromise", "StrPromise", "QuerySetAny", "ValuesQuerySet"]
