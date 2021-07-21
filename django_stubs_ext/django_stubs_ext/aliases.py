import typing

if typing.TYPE_CHECKING:
    from django.db.models.query import _T, _QuerySet, _Row

    ValuesQuerySet = _QuerySet[_T, _Row]
else:
    from django.db.models.query import QuerySet

    ValuesQuerySet = QuerySet
