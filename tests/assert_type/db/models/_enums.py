from typing import Literal

from django.db.models import TextChoices
from django.utils.functional import _StrOrPromise
from typing_extensions import assert_type


class Direction(TextChoices):
    NORTH = "N", "North"
    EAST = "E", "East"
    SOUTH = "S", "South"
    WEST = "W", "West"


assert_type(Direction.names, list[str])
assert_type(Direction.labels, list[_StrOrPromise])
assert_type(Direction.values, list[str])
assert_type(Direction.choices, list[tuple[str, _StrOrPromise]])
assert_type(Direction.NORTH, Literal[Direction.NORTH])
assert_type(Direction.NORTH.name, Literal["NORTH"])
assert_type(Direction.NORTH.label, _StrOrPromise)
assert_type(Direction.NORTH.value, str)
assert_type(Direction.NORTH.do_not_call_in_templates, Literal[True])
