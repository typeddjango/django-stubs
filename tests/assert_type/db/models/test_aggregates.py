from __future__ import annotations

from django.db.models import F
from django.db.models.aggregates import Aggregate

Aggregate("title", order_by="title")
Aggregate("title", order_by="-title")
Aggregate("title", order_by=F("title"))
Aggregate("title", order_by=F("title").desc())
Aggregate("title", order_by=["-title", F("title")])
Aggregate("title", order_by=("-title", F("title").desc()))
Aggregate("title", order_by=None)
