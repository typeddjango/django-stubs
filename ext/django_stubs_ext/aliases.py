from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from django.contrib.admin.options import _FieldOpts as FieldOpts
    from django.contrib.admin.options import _FieldsetSpec as FieldsetSpec
    from django.db.models.query import _QuerySet
    from django.test.client import _MonkeyPatchedASGIResponse as AsyncClientResponse
    from django.test.client import _MonkeyPatchedWSGIResponse as ClientResponse
    from django.utils.functional import _StrOrPromise as StrOrPromise
    from django.utils.functional import _StrPromise as StrPromise

    # Deprecated type aliases. Use the QuerySet class directly instead.
    QuerySetAny = _QuerySet
    ValuesQuerySet = _QuerySet
else:
    from django.db.models.query import QuerySet
    from django.http.response import HttpResponseBase as ClientResponse
    from django.utils.functional import Promise as StrPromise

    AsyncClientResponse = ClientResponse
    StrOrPromise = str | StrPromise
    FieldOpts = dict
    FieldsetSpec = list
    # Deprecated type aliases. Use the QuerySet class directly instead.
    QuerySetAny = QuerySet
    ValuesQuerySet = QuerySet

__all__ = [
    "AsyncClientResponse",
    "ClientResponse",
    "FieldOpts",
    "FieldsetSpec",
    "QuerySetAny",
    "StrOrPromise",
    "StrPromise",
    "ValuesQuerySet",
]
