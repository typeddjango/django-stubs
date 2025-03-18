from typing import Literal

from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _
from typing_extensions import assert_type


class MyIntegerChoices(IntegerChoices):
    A = 1
    B = 2, "B"
    C = 3, "B", "..."  # pyright: ignore[reportCallIssue]
    D = 4, _("D")
    E = 5, 1  # pyright: ignore[reportArgumentType]
    F = "1"


assert_type(MyIntegerChoices.A, Literal[MyIntegerChoices.A])
assert_type(MyIntegerChoices.A.label, str)

# For standard enums, type checkers may infer the type of a member's value
# (e.g. `MyIntegerChoices.A.value` inferred as `Literal[1]`).
# However, Django choices metaclass is using the last value for the label.
# Type checkers relies on the stub definition of the `value` property, typed
# as `int`/`str` for `IntegerChoices`/`TextChoices`.
assert_type(MyIntegerChoices.A.value, int)


class MyTextChoices(TextChoices):
    A = "a"
    B = "b", "B"
    C = "c", _("C")
    D = 1  # pyright: ignore[reportArgumentType]
    E = "e", 1  # pyright: ignore[reportArgumentType]


assert_type(MyTextChoices.A, Literal[MyTextChoices.A])
assert_type(MyTextChoices.A.label, str)
assert_type(MyTextChoices.A.value, str)


# Assertions related to the metaclass:

assert_type(MyIntegerChoices.values, list[int])
assert_type(MyIntegerChoices.choices, list[tuple[int, str]])
assert_type(MyTextChoices.values, list[str])
assert_type(MyTextChoices.choices, list[tuple[str, str]])
