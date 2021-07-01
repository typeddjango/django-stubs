import typing

if typing.TYPE_CHECKING:
    from django.db.models.query import _T, _Row, _ValuesQuerySet

    ValuesQuerySet = _ValuesQuerySet[_T, _Row]
else:
    ValuesQuerySet = typing.Any
