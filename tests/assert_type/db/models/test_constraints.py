from __future__ import annotations

from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.db.models.functions import Lower

UniqueConstraint(Lower("name").desc(), "category", name="unique_lower_name_category")
UniqueConstraint(fields=["name"], name="unique_name")
# There's no overload case for passing both expression and 'fields'
UniqueConstraint(  # type: ignore[call-overload]
    Lower("name"),
    fields=["name"],  # pyright: ignore[reportArgumentType]  # pyrefly: ignore[bad-argument-type]  # ty: ignore[invalid-argument-type]
    name="unique_mess",
)

CheckConstraint(name="positive_price", condition=Q(price__gt=0))
