from __future__ import annotations

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F

ArrayAgg("title", order_by="title")
ArrayAgg("title", order_by="-title")
ArrayAgg("title", order_by=F("title"))
ArrayAgg("title", order_by=F("title").desc())
ArrayAgg("title", order_by=["-title", F("title")])
ArrayAgg("title", order_by=("-title", F("title").desc()))
