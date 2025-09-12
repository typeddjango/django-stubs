from typing import Any

from django.db.models import CheckConstraint, F, UniqueConstraint
from django.db.models.functions import Lower
from django.db.models.lookups import LessThan

UniqueConstraint(Lower("name").desc(), "category", name="unique_lower_name_category")
UniqueConstraint(fields=["name"], name="unique_name")
# There's no overload case for passing both expression and 'fields'
UniqueConstraint(  # type: ignore[call-overload]
    Lower("name"),
    fields=["name"],  # pyright: ignore[reportArgumentType]
    name="unique_mess",
)

CheckConstraint(  # type: ignore[deprecated]  # pyright: ignore[reportDeprecated]
    name="less_than_constraint",
    check=LessThan[Any](F("months"), 1),
)
