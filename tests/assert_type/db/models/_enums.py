from typing import Literal

from django.db.models import TextChoices
from typing_extensions import assert_type


class Direction(TextChoices):
    NORTH = "N", "North"
    EAST = "E", "East"
    SOUTH = "S", "South"
    WEST = "W", "West"


# Note: Suppress errors from pyright as the mypy plugin narrows the type of labels if non-lazy.
assert_type(Direction.names, list[str])
assert_type(Direction.labels, list[str])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Direction.values, list[str])
assert_type(Direction.choices, list[tuple[str, str]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Direction.NORTH, Literal[Direction.NORTH])
assert_type(Direction.NORTH.name, Literal["NORTH"])
assert_type(Direction.NORTH.label, str)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Direction.NORTH.value, str)
assert_type(Direction.NORTH.do_not_call_in_templates, Literal[True])
