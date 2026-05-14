from __future__ import annotations

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Q

# ArrayAgg: order_by accepts single str/Combinable or sequence of either
ArrayAgg("title", order_by="title")
ArrayAgg("title", order_by="-title")
ArrayAgg("title", order_by=F("title"))
ArrayAgg("title", order_by=F("title").desc())
ArrayAgg("title", order_by=["-title", F("title")])
ArrayAgg("title", order_by=("-title", F("title").desc()))
# Aggregate kwargs forwarded through OrderableAggMixin
ArrayAgg("title", distinct=True, filter=Q(active=True), order_by="-title", default=[])
ArrayAgg("title", order_by=123)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
ArrayAgg("title", order_by=[123])  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
ArrayAgg("title", filter=F("a"))  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
ArrayAgg("title", filter="active")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
