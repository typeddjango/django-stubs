import enum
from typing import Any, Literal

from django.db.models import Choices, IntegerChoices, TextChoices
from django.utils.functional import _StrOrPromise
from django.utils.translation import gettext_lazy as _
from typing_extensions import assert_type

# Choices in a separate model to test that the plugin resolves types correctly.
from tests.assert_type.db.models import _enums as imported


class Suit(IntegerChoices):
    DIAMOND = 1, _("Diamond")
    SPADE = 2, _("Spade")
    HEART = 3, _("Heart")
    CLUB = 4, _("Club")


class YearInSchool(TextChoices):
    FRESHMAN = "FR", _("Freshman")
    SOPHOMORE = "SO", _("Sophomore")
    JUNIOR = "JR", _("Junior")
    SENIOR = "SR", _("Senior")
    GRADUATE = "GR", _("Graduate")


class Vehicle(IntegerChoices):
    CAR = 1, "Carriage"
    TRUCK = 2
    JET_SKI = 3

    __empty__ = _("(Unknown)")


class Gender(TextChoices):
    MALE = "M"
    FEMALE = "F"
    NOT_SPECIFIED = "X"

    __empty__ = "(Undeclared)"


class Medal(TextChoices):
    GOLD = enum.auto()
    SILVER = enum.auto()
    BRONZE = enum.auto()


class Separator(bytes, Choices):
    FS = b"\x1c", "File Separator"
    GS = b"\x1d", "Group Separator"
    RS = b"\x1e", "Record Separator"
    US = b"\x1f", "Unit Separator"


class Constants(float, Choices):
    PI = 3.141592653589793, "π"
    TAU = 6.283185307179586, "τ"

    __empty__ = "NULL"


class BaseEmptyChoices(Choices):
    __empty__ = "Python's None"


class VoidChoices(BaseEmptyChoices):
    ABYSS = enum.auto()
    CHASM = enum.auto()


# Choice type that has been aliased to test that the plugin resolves types correctly.
CompassPoint = imported.Direction


# Choice type that has been aliased by type to test that the plugin resolves types correctly.
Award: type[TextChoices] = Medal


# Assertions for an integer choices type that uses a lazy translatable string for all labels.
assert_type(Suit.names, list[str])
assert_type(Suit.labels, list[_StrOrPromise])
assert_type(Suit.values, list[int])
assert_type(Suit.choices, list[tuple[int, _StrOrPromise]])
assert_type(Suit.CLUB, Literal[Suit.CLUB])
assert_type(Suit.CLUB.name, Literal["CLUB"])
assert_type(Suit.CLUB.label, _StrOrPromise)
assert_type(Suit.CLUB.value, int)
assert_type(Suit.CLUB.do_not_call_in_templates, Literal[True])

# Assertions for a text choices type that uses a lazy translatable string for all labels.
assert_type(YearInSchool.names, list[str])
assert_type(YearInSchool.labels, list[_StrOrPromise])
assert_type(YearInSchool.values, list[str])
assert_type(YearInSchool.choices, list[tuple[str, _StrOrPromise]])
assert_type(YearInSchool.SENIOR, Literal[YearInSchool.SENIOR])
assert_type(YearInSchool.SENIOR.name, Literal["SENIOR"])
assert_type(YearInSchool.SENIOR.label, _StrOrPromise)
assert_type(YearInSchool.SENIOR.value, str)
assert_type(YearInSchool.SENIOR.do_not_call_in_templates, Literal[True])

# Assertions for an integer choices type that defines `__empty__`, generates most labels, etc.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
assert_type(Vehicle.names, list[str])
assert_type(Vehicle.labels, list[_StrOrPromise])
assert_type(Vehicle.values, list[int | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Vehicle.choices, list[tuple[int | None, _StrOrPromise]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Vehicle.CAR, Literal[Vehicle.CAR])
assert_type(Vehicle.CAR.name, Literal["CAR"])
assert_type(Vehicle.CAR.label, _StrOrPromise)
assert_type(Vehicle.CAR.value, int)
assert_type(Vehicle.CAR.do_not_call_in_templates, Literal[True])
assert_type(Vehicle.__empty__, _StrOrPromise)

# Assertions for an text choices type that defines `__empty__` and uses plain strings for all labels.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
assert_type(Gender.names, list[str])
assert_type(Gender.labels, list[_StrOrPromise])
assert_type(Gender.values, list[str | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Gender.choices, list[tuple[str | None, _StrOrPromise]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Gender.MALE, Literal[Gender.MALE])
assert_type(Gender.MALE.name, Literal["MALE"])
assert_type(Gender.MALE.label, _StrOrPromise)
assert_type(Gender.MALE.value, str)
assert_type(Gender.MALE.do_not_call_in_templates, Literal[True])
assert_type(Gender.__empty__, _StrOrPromise)

# Assertions for a text choices type that uses `enum.auto()`.
assert_type(Medal.names, list[str])
assert_type(Medal.labels, list[_StrOrPromise])
assert_type(Medal.values, list[str])
assert_type(Medal.choices, list[tuple[str, _StrOrPromise]])
assert_type(Medal.GOLD, Literal[Medal.GOLD])
assert_type(Medal.GOLD.name, Literal["GOLD"])
assert_type(Medal.GOLD.label, _StrOrPromise)
assert_type(Medal.GOLD.value, str)
assert_type(Medal.GOLD.do_not_call_in_templates, Literal[True])

# Assertions for a choices type that uses a custom base type.
# Note: Suppress errors from pyright as the mypy plugin handles propagating custom base types.
assert_type(Separator.names, list[str])
assert_type(Separator.labels, list[_StrOrPromise])
assert_type(Separator.values, list[bytes])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.choices, list[tuple[bytes, _StrOrPromise]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.FS, Literal[Separator.FS])
assert_type(Separator.FS.name, Literal["FS"])
assert_type(Separator.FS.label, _StrOrPromise)
assert_type(Separator.FS.value, bytes)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Separator.FS.do_not_call_in_templates, Literal[True])

# Assertions for a choices type uses a custom base type and defines `__empty__`.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
# Note: Suppress errors from pyright as the mypy plugin handles propagating custom base types.
assert_type(Constants.names, list[str])
assert_type(Constants.labels, list[_StrOrPromise])
assert_type(Constants.values, list[float | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.choices, list[tuple[float | None, _StrOrPromise]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.PI, Literal[Constants.PI])
assert_type(Constants.PI.name, Literal["PI"])
assert_type(Constants.PI.label, _StrOrPromise)
assert_type(Constants.PI.value, float)  # pyright: ignore[reportAssertTypeFailure]
assert_type(Constants.PI.do_not_call_in_templates, Literal[True])
assert_type(Constants.__empty__, _StrOrPromise)

# Assertions for a choices type where `__empty__` is defined on a base class.
# Note: Suppress errors from pyright as the mypy plugin handles making types optional.
assert_type(VoidChoices.names, list[str])
assert_type(VoidChoices.labels, list[_StrOrPromise])
assert_type(VoidChoices.values, list[Any | None])  # pyright: ignore[reportAssertTypeFailure]
assert_type(VoidChoices.choices, list[tuple[Any | None, _StrOrPromise]])  # pyright: ignore[reportAssertTypeFailure]
assert_type(VoidChoices.ABYSS, Literal[VoidChoices.ABYSS])
assert_type(VoidChoices.ABYSS.name, Literal["ABYSS"])
assert_type(VoidChoices.ABYSS.label, _StrOrPromise)
assert_type(VoidChoices.ABYSS.value, Any)
assert_type(VoidChoices.ABYSS.do_not_call_in_templates, Literal[True])
assert_type(VoidChoices.__empty__, _StrOrPromise)

# Assertions for a choices type imported from another module to test the plugin resolves correctly.
assert_type(imported.Direction.names, list[str])
assert_type(imported.Direction.labels, list[_StrOrPromise])
assert_type(imported.Direction.values, list[str])
assert_type(imported.Direction.choices, list[tuple[str, _StrOrPromise]])
assert_type(imported.Direction.NORTH, Literal[imported.Direction.NORTH])
assert_type(imported.Direction.NORTH.name, Literal["NORTH"])
assert_type(imported.Direction.NORTH.label, _StrOrPromise)
assert_type(imported.Direction.NORTH.value, str)
assert_type(imported.Direction.NORTH.do_not_call_in_templates, Literal[True])

# Assertions for a choices type aliased from another to test the plugin resolves correctly.
assert_type(CompassPoint.names, list[str])
assert_type(CompassPoint.labels, list[_StrOrPromise])
assert_type(CompassPoint.values, list[str])
assert_type(CompassPoint.choices, list[tuple[str, _StrOrPromise]])
assert_type(CompassPoint.NORTH, Literal[imported.Direction.NORTH])
assert_type(CompassPoint.NORTH.name, Literal["NORTH"])
assert_type(CompassPoint.NORTH.label, _StrOrPromise)
assert_type(CompassPoint.NORTH.value, str)
assert_type(CompassPoint.NORTH.do_not_call_in_templates, Literal[True])

# Assertions for a choices type aliased by type to test the plugin resolves correctly.
assert_type(Award.names, list[str])
assert_type(Award.labels, list[_StrOrPromise])
assert_type(Award.values, list[str])
assert_type(Award.choices, list[tuple[str, _StrOrPromise]])
