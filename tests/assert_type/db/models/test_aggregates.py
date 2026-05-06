from __future__ import annotations

from django.db.models import Count, F, Q, StdDev, StringAgg, Variance
from django.db.models.aggregates import Aggregate

Aggregate("title", order_by="title")
Aggregate("title", order_by="-title")
Aggregate("title", order_by=F("title"))
Aggregate("title", order_by=F("title").desc())
Aggregate("title", order_by=["-title", F("title")])
Aggregate("title", order_by=("-title", F("title").desc()))
Aggregate("title", order_by=None)

# Count: filter is positional-or-keyword (unique to Count)
Count("id", distinct=True)
Count("id", filter=Q(active=True))
Count("id", Q(active=True))  # filter as positional
Count(123)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
Count("id", filter="active")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
Count("id", filter=F("a"))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

# StdDev: second positional is `sample: bool`, not filter; filter/default are keyword-only
StdDev("score", filter=Q(active=True), default=0)
StdDev([])  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
StdDev("score", Q(active=True))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

# Variance: same shape as StdDev
Variance("score", filter=Q(active=True), default=0)
Variance({})  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]

# StringAgg: full Aggregate kwarg surface (distinct, filter, default, order_by)
StringAgg("title", delimiter=",", order_by="title")
StringAgg("title", delimiter=",", order_by=F("title"))
StringAgg("title", delimiter=",", order_by=["-title", F("title")])
StringAgg("title", delimiter=",", distinct=True, filter=Q(active=True), order_by="-title", default="")
StringAgg("title", delimiter=",", filter=F("a"))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
StringAgg("title", delimiter=",", order_by=123)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
